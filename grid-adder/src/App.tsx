import { useState, useEffect } from 'react'
import Camera from './components/Camera'
import ImageDisplay from './components/ImageDisplay'
import './App.css'

function App() {
  const switchToImage = () => setCurrentMode('image')
  const switchToCamera = () => setCurrentMode('camera')
  
  const [currentMode, setCurrentMode] = useState('camera')
  const [currentImage, setCurrentImage] = useState<HTMLCanvasElement | null>(null)

  return (
    <div>
      {currentMode === 'camera' ? (
        <Camera 
          onSwitchMode={switchToImage}
          setCurrentImage={setCurrentImage}
          />
          ) : (
            <ImageDisplay 
            onSwitchMode={switchToCamera}
            image={currentImage}
        />
      )}
    </div>
  )
}

export default App
