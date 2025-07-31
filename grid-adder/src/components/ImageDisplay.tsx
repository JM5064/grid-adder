import { useState, useEffect } from "react";
import BackButton from "./BackButton";
import BoundingBoxSelector from "./BoundingBoxSelector";
import { type BoundingBox } from "../types/BoundingBox";

interface ImageDisplayProps {
  onSwitchMode: () => void
  image: HTMLCanvasElement | null
}


const ImageDisplay = ({ onSwitchMode, image }: ImageDisplayProps) => {
  const [url, setUrl] = useState<string>("")
  const [boundingBox, setBoundingBox] = useState<BoundingBox | null>(null)
  const [currentSum, setCurrentSum] = useState(0)

  useEffect(() => {
    if (!image) {
      return
    }

    setUrl(image.toDataURL("image/jpeg"))
  }, [image])

  useEffect(() => {
    const processImage = async () => {
      if (!image || !boundingBox) {
        return
      }

      const sum = await getSum(image)
      if (!sum) {
        console.log("Error getting sum")
        return
      }
      
      setCurrentSum(sum)
    }

    processImage()
  }, [boundingBox])

  const getSum = async (canvas: HTMLCanvasElement): Promise<number | null> => {
    if (!canvas || canvas.width === 0 || canvas.height === 0) {
      console.log("Canvas not ready")
      return null
    }

    if (!boundingBox) {
      console.log("Bounding box not ready", image, boundingBox)
      return null
    }

    try {
      const response = await fetch('https://grid-adder.onrender.com/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: canvas.toDataURL(), boundingBox: boundingBox })
      });
  
      const data = await response.json();
      console.log("Data received:", data)
      return typeof data.result === 'number' ? data.result : null;
    } catch (error) {
      console.error('Failed to get sum:', error)
      return null
    }
  }

  if (url.length == 0) {
    return (
      <>
        <div>No current image!</div>
        <BackButton handleClick={onSwitchMode}/>
      </>
    )
  }

  return (
    <>
      {
        boundingBox ? 
          <>
            <img src={url} alt="result" className="absolute top-0 left-0 w-full h-full object-cover" /> :
    
            <div className="absolute inset-0 flex items-center justify-center">
              <h1 className="text-blue-500 text-6xl font-bold">{currentSum}</h1>
            </div>
            
            <BackButton handleClick={onSwitchMode}/>
          </>
          :
          <BoundingBoxSelector
            imageUrl={url}
            onConfirm={setBoundingBox}
          />
      }
    </>
  )

}

export default ImageDisplay

