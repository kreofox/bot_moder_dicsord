#-------
# Основное
#-------


#ТОКЕН БОТ
from pickle import TRUE


TOKEN='MTAwNTQxNzEwMzUyNTk0NTQ4NA.GZTD78.pWNm8cV6Mogy4LSdLr5Lx4_3hVPZ3Fvrv9pnyI'

#Префикс для командыю.
PREFIX='!'

#удалияет сообщения с командой перед выводом ответа?
DELETE_COMMANDS=True

#-------
#Модерация
#------

# ID роли, которая будет выдаваться участнику при муте. Для корректной работы роль не должна иметь права
# "Отправлять сообщения" и "Отправлять TTS сообщения".
MUTE_ROLE_ID = 1005798758841331782

# Отправлять личные сообщения участникам при наказаниях и их отмене.
SEND_PUNISHMENT_PERSONAL_MESSAGE = True

# ---------------
# Фильтрация чата
# ---------------

# Использовать фильтрацию чата?
USE_CHAT_FILTRATION = True

# Список плохих слов в нижнем регистре.
BAD_WORD_LIST = ('some_word', 'bad_word', 'the_worst_word')
