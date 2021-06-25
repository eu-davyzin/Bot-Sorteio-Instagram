from instagram_private_api import Client
import random
import re

usuario = 'dev_clean_code'
senha = 'davyzinho456'

api = Client(usuario, senha)

UUID = api.generate_uuid() # Necessário para a API
followers = api.user_followers(api.authenticated_user_id, rank_token=UUID)['users'] # Lista de usuários que seguem o perfil do Neps.
followers = [follower['pk'] for follower in followers] # Mas queremos uma lista apenas com o ID dos usuários

POST_CODE =  "CM2slwlgamj"
post_id = None

feed = api.self_feed() # Primeiro pegamos todas as postagens no nosso feed.
for item in feed['items']: # Iteramos em cada postagem.
	if item['code'] == POST_CODE: # Se a postagem tem _code_ igual a POST_CODE
		post_id = item['id'] # Salvamos o ID dessa postagem na variável post_id
		break

users_valid_comments = []

comments = api.media_n_comments(post_id, n=100) # Vamos pegar os 100 primeiros comentários do nosso post(customizável)
for comment in comments:	    
    match = re.findall(r"(@\w*)", comment['text']) # Checar se o usuário marcou duas pessoas usando regex
    if(len(match) >= 2 and comment['user_id'] in followers): # Se o usuário realmente marcou duas pessoas e segue o perfil do Neps, adicionamos ele nos comentários válidos
        users_valid_comments.append(comment['user_id'])

random.shuffle(users_valid_comments)

winners = set()

i = 0
while len(winners) < 1: # Enquanto nosso conjunto de vencedores tem menos que 5 pessoas
	if users_valid_comments[i] not in winners: # Se a pessoa ainda não está no nosso conjunto de vencedores adicionamos ele
		winners.add(users_valid_comments[i])
	i += 1 # Vamos para o próxima pessoa

for winner_id in winners: # Para cada vencedor
    winner = api.user_info(winner_id)['user'] # Use a API para pegar informações detalhadas dessa pessoa
    print(f"\n\nO Vencedor é {winner['full_name']} (@{winner['username']})\n\n") # Imprima nome completo e nome de usuário no Instagram.