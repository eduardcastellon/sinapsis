��          L      |       �   e  �   [        k      �     �  ;  �  m  �  ^   W  *   �  +   �                                              
% set access_url = object.get_task_url() or ''
<p>Dear ${object.user_id.name},</p>

<br>

<p>The task <a href="${access_url}">#${str(object.id) + " " + object.name}</a> with the progress ${object.progress}% has exceeded the configured limit threshold. </p>

<br>

<p>This email has been generated automatically, please do not replay.</p>
<p>Thank you,</p>
 ${object.company_id.name} Thresold Limit Exceeded on #${str(object.id) + " " + object.name} Next Thresold Reminder Date Project Task - Thresold Reminder Task Project-Id-Version: Odoo Server 13.0+e-20201021
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2021-10-14 15:44+0200
Language-Team: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n != 1);
X-Generator: Poedit 2.3
Last-Translator: 
Language: es
 
% set access_url = object.get_task_url() or ''
<p>Estimado ${object.user_id.name},</p>

<br>

<p>La tarea <a href="${access_url}">#${str(object.id) + " " + object.name}</a> con un progreso ${object.progress}% ha sobrepasado el limite de humbral configurado. </p>

<br>

<p>Este correo ha sido generado automáticamente, por favor no contestar.</p>
<p>Gracias,</p>
 ${object.company_id.name} Limite de humbral excedido en #${str(object.id) + " " + object.name} Siguiente fecha de recordatorio de humbral Tarea de proyecto - Recordatorio de humbral Tarea 