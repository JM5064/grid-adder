import { useRef, useEffect } from 'react'
import CaptureButton from './CaptureButton'
import OutlineOverlay from './OutlineOverlay'

interface CameraProps {
  onSwitchMode: () => void
  setCurrentImage: React.Dispatch<React.SetStateAction<HTMLCanvasElement | null>>
}


const Camera = ({ onSwitchMode, setCurrentImage }: CameraProps) => {

  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const streamRef = useRef<MediaStream | null>(null)

  // Initialize video feed
  useEffect(() => {
    async function init() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: 'environment',
            width: { ideal: 2450 },
            height: { ideal: 1440 }
          }
        })
  
        streamRef.current = stream
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          videoRef.current.onplay = () => {
            requestAnimationFrame(updateCanvas)
          }
        }
      } catch (error) {
        console.log("Error initializing", error)
      }
    }

    init()
  }, [])

  const updateCanvas = () => {
    if (videoRef.current && canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d')
      if (ctx) {
        canvasRef.current.width = videoRef.current.width
        canvasRef.current.height = videoRef.current.height
        ctx.drawImage(videoRef.current, 0, 0)
      }
    }

    requestAnimationFrame(updateCanvas)
  }

  const handleClick = () => {
    const processingCanvas = captureFrame()
    if (!processingCanvas) {
      return
    }

    console.log("Image set to", processingCanvas)
    setCurrentImage(processingCanvas)
    onSwitchMode()
  }

  const captureFrame = (): HTMLCanvasElement | null => {
    if (!canvasRef.current || !videoRef.current) {
      console.log("Canvas not ready")
      return null
    }

    const processingCanvas = document.createElement('canvas')
    const video = videoRef.current
    const ctx = processingCanvas.getContext('2d')!

    processingCanvas.width = video.videoWidth
    processingCanvas.height = video.videoHeight
    ctx.drawImage(video, 0, 0)

    return processingCanvas
  }

  return (
    <div className='relative w-full h-full h-screen bg-black'>
      <video ref={videoRef} autoPlay playsInline muted className='w-full '/>
      <canvas ref={canvasRef} className='absolute top-0 left-0 w-full'/>

      {/* <OutlineOverlay /> */}
      <CaptureButton handleClick={handleClick}/>
    </div>
  )
}

export default Camera