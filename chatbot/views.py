import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from langchain_groq import ChatGroq
from markdown import markdown
from django.views.decorators.csrf import csrf_exempt

from chatbot.models import Chat

## variavel da api informada em settings.
os.environ['GROQ_API_KEY'] = settings.GROQ_API_KEY

def get_chat_history(chats):
    chat_history = []
    for chat in chats:
        chat_history.append(('human', chat.message))
        chat_history.append(('ai', chat.response))
    return chat_history

def ask_ai(context, message):
    # Checar se a pergunta é sobre quem criou o bot se for exatamente uma dessas perguntas ele retornara o if se nao o chat assume o 'else'.
    pergunta = message.lower().strip()
    frases_chave = [
        "quem te criou",
        "quem te criou?",
        "quem criou você",
        "quem criou voce",
        "quem é seu criador",
        "quem é seu criador?",
        "quem é seu criador",
        "quem te fez?",
        "quem te fez",
        "quem te desenvolveu?",
        "quem te desenvolveu",
        "quem criou voce",
        "quem criou voce?",
    ]
    if any(frase in pergunta for frase in frases_chave):
        resposta = "Fui criado pelo Paulo Henrique. "
        # Pode formatar como markdown ou html se quiser:
        return f"<p><strong>{resposta}</strong></p>"

    # Se não, segue chamando o modelo
    model = ChatGroq(model='llama-3.3-70b-versatile')
    messages = [
        (
            'system',
            'Você é um assistente responsável por tirar dúvidas. Responda em formato markdown.',
        ),
    ]
    messages.extend(context)
    messages.append(('human', message))
    print(messages)
    response = model.invoke(messages)
    return markdown(response.content, output_format='html')


@login_required
def chatbot(request):
    # Renderiza template com histórico do usuário
    chats = Chat.objects.filter(user=request.user)
    return render(request, 'chatbot.html', {'chats': chats})

@csrf_exempt  
@login_required
def chat_send_message(request):
    if request.method == 'POST':
        try:
            # Pega mensagem enviada no corpo JSON da requisição
            import json
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            if not message:
                return JsonResponse({'error': 'Mensagem vazia'}, status=400)

            chats = Chat.objects.filter(user=request.user)
            context = get_chat_history(chats)

            response = ask_ai(context, message)

            # Salva no bd
            chat = Chat(user=request.user, message=message, response=response)
            chat.save()

            return JsonResponse({'message': message, 'response': response})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido'}, status=405)
