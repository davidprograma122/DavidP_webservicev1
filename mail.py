import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request # type: ignore
import os
import pickle

# Scopes necesarios para enviar correos
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def autenticar_gmail():
   
    creds = None

    # El archivo token.pickle guarda el acceso de usuario
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Si no hay credenciales válidas, pide autorización
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)

        # Guarda el acceso para la próxima vez
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service

def crear_mensaje_con_adjunto(destinatario, asunto, cuerpo_html, archivo_pdf_path=None):
    
    mensaje = MIMEMultipart()
    mensaje['to'] = destinatario
    mensaje['subject'] = asunto

    # Cuerpo del mensaje en HTML
    cuerpo = MIMEText(cuerpo_html, 'html', 'utf-8')
    mensaje.attach(cuerpo)

    # Adjuntar PDF si se proporciona
    if archivo_pdf_path and os.path.exists(archivo_pdf_path):
        with open(archivo_pdf_path, 'rb') as pdf_file:
            pdf_adjunto = MIMEApplication(pdf_file.read(), _subtype='pdf')
            pdf_adjunto.add_header('Content-Disposition', 'attachment',
                                   filename=os.path.basename(archivo_pdf_path))
            mensaje.attach(pdf_adjunto)

    # Codificar en base64
    mensaje_bytes = mensaje.as_bytes()
    mensaje_base64 = base64.urlsafe_b64encode(mensaje_bytes).decode()
    return {'raw': mensaje_base64}

def enviar_correo_orden(destinatario, numero_orden, conductor_nombre,
                        ciudad, destino, fecha_inicio, fecha_fin,
                        archivo_pdf_path=None):
    
    asunto = f"Orden de Movilización N° {numero_orden}"

    # Cuerpo
    cuerpo_html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <p>Estimado/a <strong>{conductor_nombre}</strong>,</p>

        <p>
          Se le ha asignado la orden de movilización <strong>N° {numero_orden}</strong>
          con vigencia desde el <strong>{fecha_inicio}</strong> hasta el <strong>{fecha_fin}</strong>.
        </p>

        <p>Por favor, revise el archivo adjunto para conocer todos los detalles de la orden.</p>

        <p>Atentamente,</p>
        <p><strong>Sistema de Gestión Vehicular - SENAE</strong></p>

        <hr style="margin-top: 30px; border: none; border-top: 1px solid #ccc;">

        <p style="font-size: 11px; color: #888;">
          Este es un mensaje automático. Por favor no responda a este correo.
        </p>
      </body>
    </html>
    """

    try:
        service = autenticar_gmail()
        mensaje = crear_mensaje_con_adjunto(destinatario, asunto, cuerpo_html, archivo_pdf_path)

        enviado = service.users().messages().send(userId="me", body=mensaje).execute()

        return {
            'exito': True,
            'mensaje': 'Email enviado correctamente',
            'id_mensaje': enviado["id"]
        }
    except Exception as e:
        return {
            'exito': False,
            'mensaje': f'Error al enviar email: {str(e)}',
            'id_mensaje': None
        }
