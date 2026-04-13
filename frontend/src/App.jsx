import { useState } from 'react';
import axios from 'axios';

function App() {
  const [idea, setIdea] = useState('');
  const [loading, setLoading] = useState(false);
  const [slides, setSlides] = useState([]);

  const handleGenerate = async () => {
    if (!idea) return alert("Please enter an idea first!");
    setLoading(true);
    try {
      // REPLACE the URL below with your actual Render URL
      const response = await axios.post('https://cuemath-studio-2.onrender.com//generate-creative', {
        idea: idea,
        format: 'carousel'
      });
      
      const parsedData = JSON.parse(response.data.data);
      setSlides(parsedData.slides);
    } catch (error) {
      console.error("Error generating creative:", error);
      alert("Something went wrong! Check your Render logs.");
    }
    setLoading(false);
  };

  return (
    <div style={{ 
      minHeight: '100vh', 
      backgroundColor: '#0a0a0a', 
      color: '#ffffff', 
      fontFamily: 'Inter, system-ui, sans-serif',
      padding: '40px 20px' 
    }}>
      <div style={{ maxWidth: '1000px', margin: '0 auto', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '10px' }}>Cuemath Social Media Studio</h1>
        <p style={{ opacity: 0.7, marginBottom: '30px' }}>Turn your messy ideas into polished carousels</p>
        
        <div style={{ marginBottom: '40px' }}>
          <textarea 
            rows="3" 
            placeholder="e.g., Explain why kids forget math concepts using the forgetting curve..."
            value={idea}
            onChange={(e) => setIdea(e.target.value)}
            style={{ 
              width: '100%', 
              padding: '20px', 
              borderRadius: '12px', 
              border: '1px solid #333',
              backgroundColor: '#1a1a1a',
              color: 'white',
              fontSize: '1rem',
              outline: 'none'
            }}
          />
          <button 
            onClick={handleGenerate} 
            disabled={loading} 
            style={{ 
              marginTop: '20px', 
              padding: '12px 40px', 
              borderRadius: '30px',
              border: 'none',
              backgroundColor: '#ffffff',
              color: '#000',
              fontWeight: 'bold',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
          >
            {loading ? 'Designing Slides...' : 'Create Visuals'}
          </button>
        </div>

        {/* The Carousel Canvas */}
        <div style={{ 
          display: 'flex', 
          gap: '20px', 
          overflowX: 'auto', 
          padding: '20px 0',
          scrollbarWidth: 'thin'
        }}>
          {slides.map((slide, index) => (
            <div key={index} style={{
              minWidth: '320px',
              height: '480px',
              backgroundColor: '#002E5D', // Cuemath Brand Blue
              borderRadius: '20px',
              padding: '30px',
              display: 'flex',
              flexDirection: 'column',
              boxShadow: '0 20px 40px rgba(0,0,0,0.4)',
              transition: 'transform 0.3s'
            }}>
              <div style={{ 
                height: '200px', 
                backgroundColor: '#eee', 
                borderRadius: '12px', 
                overflow: 'hidden',
                marginBottom: '20px'
              }}>
                <img 
                  src={`https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&q=80&w=400&h=400&sig=${index}`} 
                  alt="Math Visual"
                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                />
              </div>
              <div style={{ textAlign: 'left' }}>
                <span style={{ fontSize: '0.8rem', opacity: 0.6, textTransform: 'uppercase' }}>Slide {slide.slide_number}</span>
                <p style={{ fontSize: '1.4rem', fontWeight: '700', marginTop: '10px', lineHeight: '1.4' }}>
                  {slide.text}
                </p>
              </div>
              <div style={{ marginTop: 'auto', textAlign: 'left', opacity: 0.5, fontSize: '0.9rem' }}>
                Cuemath Learning Science
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;