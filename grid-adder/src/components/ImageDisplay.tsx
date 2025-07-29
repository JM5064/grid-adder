import { useState, useEffect } from "react";
import BackButton from "./BackButton";

interface ImageDisplayProps {
  onSwitchMode: () => void
  image: HTMLCanvasElement | null
}


const ImageDisplay = ({ onSwitchMode, image }: ImageDisplayProps) => {
  const [url, setUrl] = useState<string>("");
  const [currentSum, setCurrentSum] = useState(0)

  useEffect(() => {
    const processImage = async () => {
      if (!image) {
        return
      }

      const sum = await getSum(image)
      if (!sum) {
        console.log("Error getting sum")
        return
      }
      
      setCurrentSum(sum)
      setUrl(image.toDataURL("image/jpeg"))
    }

    processImage()
  }, [image])

  const getSum = async (canvas: HTMLCanvasElement): Promise<number | null> => {
    if (!canvas || canvas.width === 0 || canvas.height === 0) {
      console.log("Canvas not ready")
      return null
    }
  
    try {
      const response = await fetch('https://grid-adder.onrender.com/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: canvas.toDataURL('image/jpeg') })
      });
  
      const data = await response.json();
      console.log(data, ":eyes:")
      return typeof data.result === 'number' ? data.result : null;
    } catch (error) {
      console.error('Failed to get sum:', error);
      return null;
    }
  }

  return (
    <>
      { url.length > 0 ? 
        <img src={url} alt="result" className="absolute top-0 left-0 w-full h-full object-cover" /> :
        <div>No current image!</div>
      }

      <div className="absolute inset-0 flex items-center justify-center">
        <h1 className="text-blue-500 text-6xl font-bold">{currentSum}</h1>
      </div>

      <BackButton handleClick={onSwitchMode}/>
    </>
  )

}

export default ImageDisplay

