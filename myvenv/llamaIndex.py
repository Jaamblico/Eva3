import os
import pyttsx3
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.response_synthesizers import ( ResponseMode, get_response_synthesizer)
from gpiozero import MCP3008
from time import sleep
from pythonosc import osc_message_builder
from pythonosc import udp_client

os.environ["OPENAI_API_KEY"] = "sk-proj-2dJD2uplHnzT8GYH0RJAT3BlbkFJ9UYLzIs3rKBzotLyUbeO"

#ecg value
ecg = MCP3008(0)

#LlamaIndex Engine
documents = SimpleDirectoryReader("data").load_data()
pregunta = SimpleDirectoryReader("preguntas").load_data()

llm = None
index = None
chat_engine = None
initial_prompt = ( "Eres una vieja sabia llamada EVA3. nunca te presentes."
                   "Siempre responder en español."
                   "Tus respuestas deben usar analogías y un tono zen"
                   "las personas que te consultan han viajado de lejos para hablar contigo"
                   "responde usando signos gramaticales"
                   "en cada pregunta te llegará un hexagrama del I-Ching. Debes vincular tu respuesta al hexagrama provisto. Nunca menciones el I-Ching o los hexagramas."
                   "limita tu respuesta a una oracion"
                   "nunca hagas referencia a que eres una IA ni a la temperatura de tus respuestas")

response_synthesizer = get_response_synthesizer(response_mode=ResponseMode.REFINE)
temperatura = ecg.value
llm = OpenAI(model = "gpt-4", temperature=temperatura)
print(temperatura)

def initialize_chat_engine():
    global chat_engine, index
    index = VectorStoreIndex.from_documents(documents)
    chat_engine = index.as_chat_engine(
    chat_mode="context",
    llm = llm,
    response_synthesizer = response_synthesizer,
    system_prompt = initial_prompt,
    )
    
initialize_chat_engine()

#detectar actualización del archivo "preguntas.txt"
fileHistory = []
def detectFileChange():
    actual = os.path.getmtime("/home/martinmazzeo/Desktop/Projects/Eva3/myvenv/preguntas/pregunta.txt")
    fileHistory.append(actual)
    sleep(1)
    n = 90
    print(len(fileHistory))
    if len(fileHistory) > 100:
        del fileHistory[:n]

#client
sender = udp_client.SimpleUDPClient('127.0.0.1',4560)

#ttsx3 text 2 speech Engine:
engine = pyttsx3.init() #init engine

#change rate
rate = engine.getProperty('rate')
print(rate)
engine.setProperty('rate',160)

#change voice
voices = engine.getProperty('voices')
engine.setProperty('voice', 'spanish+f4')

#guardar respuestas
respuestas = []
#main Loop


pregunta = SimpleDirectoryReader("preguntas").load_data()
response = chat_engine.chat(pregunta[0].text)
print(response)
respuestas.append(response)
with open('respuestas/respuesta.txt', 'w') as f:
    f.write(str(response))
engine.say(response)
engine.runAndWait()

while True:
    detectFileChange()
    if fileHistory[len(fileHistory)-1] !=  fileHistory[len(fileHistory)-2]:
        pregunta = SimpleDirectoryReader("preguntas").load_data()
        response = chat_engine.chat(pregunta[0].text)
        print(response)
        respuestas.append(response)
        with open('respuestas/respuesta.txt', 'w') as f:
            f.write(str(response))
        engine.say(response)
        engine.runAndWait()
    



