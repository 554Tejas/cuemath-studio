import { useState } from 'react';
import axios from 'axios';

function App() {
  const [idea, setIdea] = useState('');
  const [loading, setLoading] = useState(false);
  const [slides, setSlides] = useState([]);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/generate-creative', {
        idea: idea,
        format: 'carousel'
      });
      
      const parsedData = JSON.parse(response.data.data);
      setSlides(parsedData.slides);
    } catch (error) {
      console.error("Error generating creative:", error);
      alert("Something went wrong!");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '40px', fontFamily: 'sans-serif' }}>
      <h1>Cuemath Social Media Studio</h1>
      
      <div style={{ marginBottom: '20px' }}>
        <textarea 
          rows="4" 
          cols="50"
          placeholder="E.g., Carousel for parents about the forgetting curve..."
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          style={{ width: '100%', padding: '10px' }}
        />
        <br />
        <button onClick={handleGenerate} disabled={loading} style={{ marginTop: '10px', padding: '10px 20px' }}>
          {loading ? 'Generating...' : 'Create Visuals'}
        </button>
      </div>

      {/* The Canvas Layout */}
      <div style={{ display: 'flex', gap: '20px', overflowX: 'auto' }}>
        {slides.map((slide) => (
          <div key={slide.slide_number} style={{
            minWidth: '300px',
            height: '300px',
            backgroundColor: '#f0f0f0',
            border: '2px solid #ddd',
            padding: '20px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'center',
            alignItems: 'center',
            textAlign: 'center'
          }}>
            <h3>Slide {slide.slide_number}</h3>
            <p>{slide.text}</p>
            {/* Future integration: Replace this paragraph with an actual <img> tag once you add image generation */}
            <p style={{ fontSize: '10px', color: 'gray' }}>Image Prompt: {slide.image_prompt}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;