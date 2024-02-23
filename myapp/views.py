from django.shortcuts import render
from .models import UserInput, GPTResponse
import openai
from decouple import config

# Use environment variable for the API key
openai.api_key = config('OPENAI_API_KEY')

def home(request):
    if request.method == 'POST':
        user_input_text = request.POST.get('user_input', '').strip()

        # Form validation
        if not user_input_text:
            return render(request, 'myapp/home.html', {'error': 'Invalid input'})

        user_input = UserInput.objects.create(text=user_input_text)

        try:
            # Make OpenAI Chat API request
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
                    {"role": "user", "content": user_input_text}
                ]
            )

            # Extract GPT response text
            gpt_response_text = completion['choices'][0]['message']['content']
            GPTResponse.objects.create(user_input=user_input, text=gpt_response_text)

        except Exception as e:
            # Handle OpenAI API errors
            return render(request, 'myapp/home.html', {'error': f'Error with OpenAI API: {e}'})

    responses = GPTResponse.objects.all().order_by('-created_at')
    return render(request, 'myapp/home.html', {'responses': responses})
