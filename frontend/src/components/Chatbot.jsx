import React, { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import { MessageCircle, X, Send } from 'lucide-react'

const Chatbot = () => {
    const [isOpen, setIsOpen] = useState(false)
    const [messages, setMessages] = useState([
        { sender: 'bot', text: 'Hi! I am AirGuard Bot. Ask me about air quality or health precautions.' }
    ])
    const [input, setInput] = useState('')
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const sendMessage = async () => {
        if (!input.trim()) return

        const userMsg = { sender: 'user', text: input }
        setMessages(prev => [...prev, userMsg])
        setInput('')

        try {
            const response = await axios.post('http://localhost:8000/api/chatbot', { message: input })
            const botMsg = { sender: 'bot', text: response.data.response }
            setMessages(prev => [...prev, botMsg])
        } catch (error) {
            setMessages(prev => [...prev, { sender: 'bot', text: "Sorry, I'm having trouble connecting to the server." }])
        }
    }

    return (
        <>
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    style={{
                        position: 'fixed',
                        bottom: '20px',
                        right: '20px',
                        borderRadius: '50%',
                        width: '60px',
                        height: '60px',
                        padding: 0,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        boxShadow: '0 4px 20px rgba(0,210,255,0.4)'
                    }}
                >
                    <MessageCircle size={30} />
                </button>
            )}

            {isOpen && (
                <div className="chatbot">
                    <div className="chat-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span>AirGuard Assistant</span>
                        <button onClick={() => setIsOpen(false)} style={{ background: 'transparent', padding: '5px', color: '#fff' }}>
                            <X size={20} />
                        </button>
                    </div>
                    <div className="chat-messages">
                        {messages.map((msg, index) => (
                            <div key={index} style={{ textAlign: msg.sender === 'user' ? 'right' : 'left' }}>
                                <div className={msg.sender === 'user' ? 'user-msg' : 'bot-msg'}>
                                    {msg.text}
                                </div>
                            </div>
                        ))}
                        <div ref={messagesEndRef} />
                    </div>
                    <div className="chat-input">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                            placeholder="Ask about AQI..."
                        />
                        <button onClick={sendMessage} style={{ marginLeft: '10px', padding: '8px' }}>
                            <Send size={18} />
                        </button>
                    </div>
                </div>
            )}
        </>
    )
}

export default Chatbot
