import datetime
import json
import os
import sys

import phonenumbers
import qrcode
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import BadRequest
from django.core.mail import EmailMultiAlternatives
from django.forms import ValidationError
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.utils import timezone
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCaptureRequest
from weasyprint import HTML

from Apps.Eventos.forms import CareerForm, EventForm, ParticipantForm
from Apps.Eventos.models import Career, Event, EventParticipant, Participant
from Apps.Users.models import User


def view_events(request):
    global get_career
    if request.user.is_superuser:
        events = Event.objects.filter()
    else:
        events = Event.objects.filter(active=True)

    data = {
        'form': EventForm(),
        'events': events,
    }

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            logo = request.FILES.get('logo')
            title = request.POST.get('title')
            place = request.POST.get('place')
            addressed_to = request.POST.get('addressed_to')
            price = request.POST.get('price')
            start_date = request.POST.get('start_date')
            final_date = request.POST.get('final_date')
            modality = request.POST.get('modality')
            country_phone = request.POST.get('country_phone')
            phone = request.POST.get('phone')
            alternative_phone = request.POST.get('alternative_phone')
            email = request.POST.get('email')
            alternative_email = request.POST.get('alternative_email') if request.POST.get('alternative_email') != '' \
                else None
            event_planning = request.FILES.get('event_planning')
            link_video = request.POST.get('link_video')
            platform_meeting = request.POST.get('platform_meeting')
            link_to_classroom = request.POST.get('link_to_classroom')
            code_meeting = request.POST.get('code_meeting')
            career = request.POST.get('career')
            teachers = request.POST.get('teachers')

            if isinstance(alternative_phone, str):
                alternative_phone = None

            get_career = None
            try:
                get_career = get_object_or_404(Career, id=career)
            except Career.DoesNotExist:
                messages.error(request, 'No se pudo encontrar la carrera seleccionada. Contacte al administrador.')
            except ValueError:
                messages.error(request, 'Porfavor selecciona una carrera válida')

            if final_date < start_date:
                raise ValidationError('La fecha final no puede ser menor a la fecha de inicio')

            event = Event(user_id=request.user.id, logo=logo, title=title, place=place,
                          addressed_to=addressed_to, price=price, start_date=start_date,
                          final_date=final_date, modality=modality, country_phone=country_phone,
                          phone=phone, alternative_phone=alternative_phone, email=email,
                          alternative_email=alternative_email, platform_meeting=platform_meeting,
                          link_to_classroom=link_to_classroom, code_meeting=code_meeting,
                          event_planning=event_planning, link_video=link_video, career=get_career,
                          )
            event.save()
            form2 = EventForm(request.POST, instance=event)
            form2.save(commit=False)
            form2.save_m2m()
            messages.success(request, 'Evento creado exitosamente')
            return redirect('eventos')
        else:
            data['form'] = form
            messages.error(request, 'Ocurrió un error. Intente de nuevo.')

    return render(request, 'Eventos/index.html', data)


@login_required
def view_event(request, id_event):
    event = get_object_or_404(Event, id=id_event)

    participants = event.eventparticipant_set.all()
    event_participant = None
    participants.filter()

    try:
        participant = get_object_or_404(Participant, user_id=request.user.id)
        try:
            event_participant = event.eventparticipant_set.get(participant=participant)
        except:
            pass
    except Exception:
        participant = None

    data = {
        'event': event,
        'participant': participant,
        'participants': participants,
        'event_participant': event_participant,
        'actives_participants': participants.filter(active=True, event=event),
        'form_participant': ParticipantForm(instance=request.user),
        'template_name_email_event': 'Eventos/contact_event_email.html',
    }

    if request.method == 'POST':
        result = validate_participant_event(request, id_event, data)
        if result == 'error':
            pass
        else:
            return redirect('view_event', id_event)

    return render(request, 'Eventos/view_event.html', data)


@login_required
@permission_required('Eventos.change_event', raise_exception=True)
def update_event(request, id_event):
    event = get_object_or_404(Event, id=id_event)
    data = {
        'form': EventForm(instance=event),
        'event': event,
    }

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            if form.has_changed():
                logo = request.FILES.get('logo') if request.FILES.get('logo') is not None else event.logo
                event_planning = request.FILES.get('event_planning') if request.FILES.get('event_planning') is not None\
                    else event.event_planning
                event_modified = form.save()
                event_modified.logo = logo
                event_modified.event_planning = event_planning
                form2 = EventForm(request.POST, instance=event)
                try:
                    event_modified.save()
                    form2.save(commit=False)
                    form2.save_m2m()
                    messages.success(request, 'Evento modificado exitosamente')
                    return redirect('view_event', event.id)
                except Exception as e:
                    messages.error(request, f'Error: {e}')
                    data['form'] = form
            else:
                messages.info(request, 'Debes propocionar información nueva para actualizar los datos.')
                return redirect('update_event', event.id)
        else:
            messages.error(request, 'Algunos datos son inválidos. Revise e intente de nuevo.')
            data['form'] = form

    return render(request, 'Eventos/update_event.html', data)


@login_required
def validate_participant_event(request, id_event, data):
    user = get_object_or_404(User, id=request.user.id)
    event = get_object_or_404(Event, id=id_event)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES)
        if form.is_valid():
            referral = None
            try:
                referral = User.objects.get(id=int(request.POST.get('referral')), is_referral=True)
            except User.DoesNotExist:
                referral = None
            except Exception as e:
                referral = None

            profile_image = request.FILES.get('profile_image') if request.FILES.get('profile_image') else \
                os.path.join(settings.MEDIA_URL, 'user_profile_placeholder.jpg')

            first_name = user.first_name if request.POST.get('first_name') == '' else request.POST.get('first_name')
            last_name = user.last_name if request.POST.get('last_name') == '' else request.POST.get('last_name')
            country_of_birth = request.POST.get('country_of_birth')
            dni = request.POST.get('dni')
            passport_number = request.POST.get('passport_number') if request.POST.get('passport_number') != '' else None
            print(passport_number)
            gender = request.POST.get('gender')
            birthdate = request.POST.get('birthdate')
            current_country = request.POST.get('current_country')
            address = request.POST.get('address')
            phone = request.POST.get('phone')
            email = user.email
            alternative_email = request.POST.get('alternative_email') if request.POST.get('alternative_email') else None
            object = request.POST.get('object')

            participant = Participant(
                user=request.user, profile_image=profile_image, first_name=first_name, last_name=last_name,
                dni=dni, country_of_birth=country_of_birth, passport_number=passport_number, gender=gender,
                birthdate=birthdate, current_country=current_country, address=address, phone=phone, email=email,
                alternative_email=alternative_email, object=object, referral=referral,
            )
            try:
                participant.save()
                if user.is_superuser or event.user.id == user.id or user.is_teacher:
                    event.participants.add(participant, through_defaults={
                        'active': True,
                        'pay': True,
                        'client_name': user.username,
                        'client_email': user.email,
                        'payer_id': user.id,
                        'total_buy': 0.00,
                        'discount_paypal': 0.00,
                        'net_price': 0.00,
                        'status_buy': 'COMPLETED',
                        'status_code': '203',
                    })
                else:
                    event.participants.add(participant, through_defaults={'active': True})
                messages.success(request, '¡Te haz regístrado exitosamente!')
            except Exception as e:
                return 'exception'
        else:
            messages.error(request, 'Ocurrió un error. Intenta de nuevo')
            data['form_participant'] = form
            return 'error'


@login_required
def set_active_participant(request, id_event):
    event = get_object_or_404(Event, id=id_event)
    participant = get_object_or_404(Participant, user_id=request.user.id)
    exists_participant = event.eventparticipant_set.filter(participant=participant.id)

    referral = None
    try:
        referral = User.objects.get(id=int(request.POST.get('referral')), is_referral=True)
    except User.DoesNotExist:
        referral = None
    except Exception as e:
        referral = None

    if exists_participant.exists():
        participant = exists_participant.get()

        if participant.active:
            try:
                participant.active = False
                participant.participant.referral = None
                participant.save()
                participant.participant.save()
                messages.success(request, '¡Fuíste elíminado de la lista de participantes exitosamente!')
            except Exception as e:
                messages.error(request,
                               'No se pudo eliminar de la lista de participantes. Contactenos por medio de un Email o '
                               'un WhatsApp')
            finally:
                return redirect('view_event', id_event)
        else:
            try:
                participant.active = True
                participant.participant.referral = referral
                participant.save()
                participant.participant.save()
                messages.success(request, '¡Fuíste añadido a la lista de participantes exitosamente!')
            except Exception as e:
                messages.error(request,
                               'No se pudo añadir a la lista de participantes. Contactenos por medio de un Email o un '
                               'WhatsApp')
            finally:
                return redirect('view_event', id_event)
    else:
        event.participants.add(participant, through_defaults={'active': True})
        participant.referral = referral
        participant.save()
        messages.success(request, '¡Fuíste añadido a la lista de participantes exitosamente!')
        return redirect('view_event', id_event)


@login_required
def download_certify_event(request, id_event, id_participant):
    event = get_object_or_404(Event, id=id_event)
    participant = get_object_or_404(Participant, id=id_participant)
    teacher_certify = False
    if event.participants.all().filter(event__teachers__username=participant.user.username):
        teacher_certify = True
    payment_data = get_object_or_404(EventParticipant, event_id=event.id, participant_id=participant.id)

    url_certify = '{0}{1}'.format(request.get_host(), request.get_full_path())
    qr_root = os.path.join(settings.MEDIA_ROOT, 'QRCODES', f'event_{event.id}_participant_{participant.id}.png')
    if not os.path.exists(qr_root):
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url_certify)
        qr.make(fit=True)
        img = qr.make_image(fill_color='black', back_color='white')
        img.save(qr_root)

    context = {
        'event': event,
        'participant': participant,
        'teacher_certify': teacher_certify,
        'payment_data': payment_data,
        'now': datetime.datetime.now(),
        'qr': os.path.join(settings.MEDIA_URL, 'QRCODES', f'event_{event.id}_participant_{participant.id}.png'),
        'certify_url': url_certify,
    }

    template = get_template('Eventos/certify.html')
    html_template = template.render(context)

    pdf = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename={0}_{1}{2}'.format('Certificado', participant.get_full_name(), '.pdf')
    messages.success(request, 'Certificado generado exitosamente.')
    return render(request, 'Eventos/certify.html', context)
    # return response


@login_required
def pago(request, id_event):
    data = json.loads(request.body)
    event = get_object_or_404(Event, id=id_event, active=True)
    participant = get_object_or_404(Participant, user_id=request.user.id)
    is_participant_registered = event.eventparticipant_set.filter(participant=participant.id)

    if is_participant_registered.exists():
        participant = is_participant_registered.get()
        if not participant.pay:
            event_name, event_price = event.title, event.price
            order_id = data['orderID']
            detail = GetOrder().get_order(order_id)
            detail_price = float(detail.result.purchase_units[0].amount.value)

            if detail_price == float(event_price):
                transaction = CaptureOrder().capture_order(order_id, debug=True)
                client_name = '{0} {1}'.format(transaction.result.payer.name.given_name,
                                               transaction.result.payer.name.surname)

                participant_buy = get_object_or_404(EventParticipant, participant=participant.participant, event=event)
                participant_buy.order_id = transaction.result.id
                participant_buy.capture_id = transaction.result.purchase_units[0].payments.captures[0].id
                participant_buy.client_name = client_name
                participant_buy.client_email = transaction.result.payer.email_address
                participant_buy.payer_id = transaction.result.payer.payer_id
                participant_buy.total_buy = transaction.result.purchase_units[0].payments.captures[0].amount.value
                participant_buy.discount_paypal = transaction.result.purchase_units[0].payments.captures[
                    0].seller_receivable_breakdown.paypal_fee.value
                participant_buy.net_price = transaction.result.purchase_units[0].payments.captures[
                    0].seller_receivable_breakdown.net_amount.value
                participant_buy.status_buy = transaction.result.status
                participant_buy.status_code = transaction.status_code
                participant_buy.active = True
                participant_buy.pay = True

                participant_buy.save()

                message = ""

                content = {
                    'event': event,
                    'message': message,
                    'current_year': timezone.now().year,
                }
                template = get_template('Eventos/email_post_pay.html')
                content_template = template.render(content)
                emails = [participant.participant.email]
                if participant.participant.alternative_email is not None:
                    emails.append(participant.participant.alternative_email)

                email = EmailMultiAlternatives(
                    subject='Email de confirmación de pago',
                    body=message, from_email=settings.EMAIL_HOST_USER, to=emails,
                    reply_to=[settings.EMAIL_HOST_USER])

                try:
                    email.attach_alternative(content_template, 'text/html')
                    email.send()
                    messages.success(request, 'Mensaje enviado exitosamente')
                except Exception as e:
                    messages.error(request, 'No se pudo enviar el mensaje. Intenta de nuevo más tarde')

                data = {
                    "icon": f"success",
                    "title": "¡Transacción exitosa!",
                    "text": f"{transaction.result.payer.name.given_name} <br>"
                            f"Total: {transaction.result.purchase_units[0].payments.captures[0].amount.value} <br>"
                            f"Fecha: {timezone.now().date()} - {timezone.now().time()}",
                    "footer": f"ID Compra {transaction.result.purchase_units[0].payments.captures[0].id}"
                }
                return JsonResponse(data)
            else:
                data = {
                    "icon": f"error",
                    "title": "¡Error de precios!",
                    "text": f"El precio a pagar por paypal no es igual al precio del evento.",
                    "footer": f"Paypal: {detail_price} - Precio real: {event_price}"
                }
                return JsonResponse(data)
        else:
            data = {
                "icon": f"warning",
                "title": "Pago ya realizado",
                "text": f"Ya realizaste el pago a este evento",
                "footer": f"Si continuas teniendo problemas, no dudes en contactarnos"
            }
            return JsonResponse(data)
    else:
        data = {
            "icon": f"warning",
            "title": "Falta Registro",
            "text": f"Antes de pagar por el evento, llena tus datos de regístro o da click en el botón 'Quiero asistir'",
            "footer": f"Si continuas teniendo problemas, no dudes en contactarnos"
        }
        return JsonResponse(data)


class PayPalClient:
    def __init__(self):
        self.client_id = "AZz1x8MxPQnQJ6KYko9_9Fqjyyvc-ufqz-aCQTzR7j0rO4rA4TkyMj1YxvRHLWQvXcRfKwyQBJNe34dy"
        self.client_secret = "ENlL3ldBnYpU_PaJ2tZ5bGS0GRlhS_-mtbh7pN9EwA9b4jMc1Emr7ZwVOxM4Abr0tHxGpVQoAHKZ4VrF"

        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key, value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else \
                self.object_to_json(value) if not self.is_primittive(value) else value
        return result

    def array_to_json_array(self, json_array):
        result = []
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if not self.is_primittive(item)
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)


# Obtener los detalles de la transacción
class GetOrder(PayPalClient):
    # 2. Set up your server to receive a call from the client
    """You can use this function to retrieve an order by passing order ID as an argument"""

    def get_order(self, order_id):
        """Method to get order"""
        request = OrdersGetRequest(order_id)
        # 3. Call PayPal to get the transaction
        response = self.client.execute(request)
        return response


class CaptureOrder(PayPalClient):
    # 2. Set up your server to receive a call from the client
    """this sample function performs payment capture on the order.
    Approved order ID should be passed as an argument to this function"""

    def capture_order(self, order_id, debug=False):
        """Method to capture order using order_id"""
        request = OrdersCaptureRequest(order_id)
        # 3. Call PayPal to capture an order
        response = self.client.execute(request)
        # 4. Save the capture ID to your database. Implement logic to save capture to your database for future
        # reference.
        return response


def send_email_event(request, id_event, template_route: str):
    template_route = template_route.replace(' ', '/', 1)
    template_route = template_route + '.html'
    template = get_template(template_route)
    event = get_object_or_404(Event, id=id_event)
    user_names = request.POST.get('user_name')
    user_email = request.POST.get('user_email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')

    content = {
        'user_names': user_names,
        'user_email': user_email,
        'subject': subject,
        'message': message,
        'event': event,
        'current_year': timezone.now().year,
    }
    content_template = template.render(content)

    emails = [event.email]
    if event.alternative_email is not None:
        emails.append(event.alternative_email)

    email = EmailMultiAlternatives(
        subject=subject, body=message, from_email=settings.EMAIL_HOST_USER, to=emails, reply_to=[user_email])

    try:
        email.attach_alternative(content_template, 'text/html')
        email.send()
        messages.success(request, 'Mensaje enviado exitosamente')
    except Exception as e:
        messages.error(request, 'No se pudo enviar el mensaje. Intenta de nuevo más tarde')

    return redirect('view_event', id_event)


def send_whatsapp_event(request, id_event):
    event = get_object_or_404(Event, id=id_event)
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        country_phone_user = request.POST.get('country_phone_user')
        number_user = request.POST.get('number_user')
        message = request.POST.get('message')

        phone_number_info = phonenumbers.parse(number_user, country_phone_user)
        full_number = '{0}{1}'.format(phone_number_info.country_code, phone_number_info.national_number)

        url = "https://api.ultramsg.com/instance40328/messages/chat"

        payload = "token=xlvb1wg94yvs92mu&to={0}&body=*{1}* \n\nLe escribe: *{2}* | Télefono: *{3}* | " \
                  "Correo: {4} \n\n_{5}_ \n\nFecha: *{6} {7}:{8}*".format(
            event.get_full_number_phone(), event.title.upper(), user_name, full_number,
            user_email, message, timezone.now().date(), timezone.now().time().hour,
            timezone.now().time().minute
        )

        payload = payload.encode('utf8').decode('iso-8859-1')
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("POST", url, data=payload, headers=headers)
        content = response.json()

        if content.get('sent') == 'true':
            messages.success(request, 'Mensaje enviado exitosamente!')
            return redirect('view_event', id_event)
        else:
            messages.error(request, 'No se pudo enviar el mensaje')
            return redirect('view_event', id_event)

    return redirect('view_event', id_event)


@login_required
def careers(request):
    all_careers = Career.objects.all()
    data = {
        'form': CareerForm(),
        'careers': all_careers,
    }

    if request.method == 'POST':
        create_careers(request, data)
        return redirect('careers')

    return render(request, 'Eventos/carreras_universitarias.html', data)


@permission_required('Eventos.add_career', raise_exception=True)
def create_careers(request, data):
    form = CareerForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        messages.success(request, '¡Carrera registrada exitosamente!')
    else:
        data['form'] = form
        messages.error(request, 'Ocurrió algún error. Intente de nuevo.')


@login_required
@permission_required('Eventos.change_career', raise_exception=True)
def update_career(request, id_career):
    career = get_object_or_404(Career, id=id_career)
    form = CareerForm(request.POST, instance=career)
    if form.is_valid():
        form.save()
        messages.success(request, '¡Carrera actualizada exitosamente!')
        return redirect('careers')
    else:
        for key, value in form.errors.items():
            print(value)
        messages.error(request, 'Ocurrió algún error. Revise e intente de nuevo.')


@login_required
@permission_required('Eventos.delete_career', raise_exception=True)
def delete_career(request, id_career):
    career = get_object_or_404(Career, id=id_career)
    career.delete()
    messages.success(request, '¡Carrera eliminada exitosamente!')
    return redirect('careers')

