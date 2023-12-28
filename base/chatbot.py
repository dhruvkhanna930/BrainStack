import google.generativeai as palm

# # # Setting up the palmAPIServer
# load_dotenv()
# try:
#     api_key_env = os.environ['CHATBOT_API_KEY']
#     palm.configure(api_key=api_key_env)
# except KeyError:
#     raise ValueError("CHATBOT_API_KEY is not set in the environment variables.")

def chatbot_v2(request):
    if request.method == 'POST':
        message = request.POST.get('message')

        defaults = {
        'model': 'models/chat-bison-001',
        'temperature': 0.25,
        'candidate_count': 1,
        'top_k': 40,
        'top_p': 0.95,
        }
        prompt = message
        context = "Speak like a helper"
        examples = []

        try:
            response = palm.chat(
            **defaults,
            messages=prompt,
            context=context,
            examples=examples,
            )
            return response.last
        except Exception as e:
            # Handle potential errors during chatbot interaction
            return f"Error interacting with the chatbot: {str(e)}"
    


# def chatbot_v2(request):
#     if request.method == 'POST':
#         message = request.POST.get('message')

#         defaults = {
#         'model': 'models/chat-bison-001',
#         'temperature': 0.25,
#         'candidate_count': 1,
#         'top_k': 40,
#         'top_p': 0.95,
#         }
#         prompt = message
#         context = "Speak like a helper"
#         examples = []

#         try:
#             response = palm.chat(
#             **defaults,
#             messages=prompt,
#             context=context,
#             examples=examples,
#             )
#             response = response.last
#         except Exception as e:
#             # Handle potential errors during chatbot interaction
#             response = f"Error interacting with the chatbot: {str(e)}"
        
#         return JsonResponse({'response':response})






    