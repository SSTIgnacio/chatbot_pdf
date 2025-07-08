import React, { useState, useEffect, useRef } from 'react';
import './index.css';

const SendIcon = () => ( <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg> );
const ResetIcon = () => ( <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="23 4 23 10 17 10"></polyline><polyline points="1 20 1 14 7 14"></polyline><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path></svg> );

function App() {
  const [messages, setMessages] = useState([{ sender: 'bot', text: 'Hola, soy tu asistente virtual. ¿Sobre qué parte de la guía de viajes accesibles te gustaría preguntar?' }]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatLogRef = useRef(null);
  const sessionIdRef = useRef(crypto.randomUUID());
  const API_BASE_URL = 'http://localhost:8001';

  useEffect(() => {
    if (chatLogRef.current) {
      chatLogRef.current.scrollTop = chatLogRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    const messageText = inputValue.trim();
    if (!messageText || isLoading) return;

    setMessages(prev => [...prev, { sender: 'user', text: messageText }]);
    setInputValue('');
    setIsLoading(true);
    setMessages(prev => [...prev, { sender: 'bot', text: '', isTyping: true }]);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageText, conversation_id: sessionIdRef.current }),
      });

      if (!response.ok) throw new Error(`Error del servidor: ${response.statusText}`);
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullBotResponse = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\\n\\n').filter(line => line.trim() !== '');
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const jsonData = line.substring(6);
            try {
              const data = JSON.parse(jsonData);
              if (data.type === 'content') {
                fullBotResponse += data.content;
                setMessages(prev => {
                  const newMessages = [...prev];
                  newMessages[newMessages.length - 1] = { sender: 'bot', text: fullBotResponse };
                  return newMessages;
                });
              } else if (data.type === 'done') {
                setIsLoading(false);
              }
            } catch (e) { console.error('Error al parsear el chunk JSON:', jsonData, e); }
          }
        }
      }
    } catch (error) {
      console.error('Error al enviar el mensaje:', error);
      let errorMessage = 'Ocurrió un error inesperado.';
      if (error.message.includes('Failed to fetch')) {
        errorMessage = 'Error de conexión: No se pudo conectar con el servidor. Por favor, asegúrate de que el backend esté funcionando.';
      } else if (error.message.includes('Error del servidor')) {
        errorMessage = `Error del servidor: ${error.message}`;
      }
      setMessages(prev => {
        const newMessages = [...prev];
        newMessages[newMessages.length - 1] = { sender: 'bot', text: errorMessage };
        return newMessages;
      });
      setIsLoading(false);
    }
  };

  const handleReset = async () => {
    setIsLoading(true);
    try {
        await fetch(`${API_BASE_URL}/reset`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conversation_id: sessionIdRef.current })
        });
        setMessages([{ sender: 'bot', text: 'La conversación ha sido reiniciada. ¿Cómo puedo ayudarte?' }]);
    } catch(error) {
        console.error("Error al reiniciar la sesión:", error);
    } finally {
        setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <header className="chat-header">
        <h1>Asistente de Viajes Accesibles</h1>
      </header>
      <main ref={chatLogRef} className="chat-log">
        {messages.map((msg, index) => (
          <div key={index} className={`message message-${msg.sender}`}>
            <div className="message-content">
              {msg.isTyping ? <div className="typing-indicator"><span></span><span></span><span></span></div> : msg.text}
            </div>
          </div>
        ))}
      </main>
      <footer className="chat-footer">
        <form onSubmit={handleSendMessage} className="chat-form">
          <input type="text" value={inputValue} onChange={(e) => setInputValue(e.target.value)} placeholder="Escribe tu pregunta aquí..." autoComplete="off" disabled={isLoading} />
          <button type="submit" title="Enviar Mensaje" disabled={isLoading}><SendIcon /></button>
          <button type="button" title="Reiniciar Conversación" onClick={handleReset} disabled={isLoading}><ResetIcon /></button>
        </form>
      </footer>
    </div>
  );
}

export default App;