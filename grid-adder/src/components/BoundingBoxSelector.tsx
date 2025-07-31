import React, { useRef, useState } from 'react'
import { type BoundingBox } from '../types/BoundingBox'

interface BoundingBoxSelectorProps {
  imageUrl: string
  onConfirm: (box: BoundingBox) => void
}

interface Point {
  x: number,
  y: number
}

const BoundingBoxSelector = ({ imageUrl, onConfirm }: BoundingBoxSelectorProps) => {
  const [firstPoint, setFirstPoint] = useState<Point | null>(null)
  const [secondPoint, setSecondPoint] = useState<Point | null>(null)
  const [boundingBox, setBoundingBox] = useState<BoundingBox | null>(null)

  const imageRef = useRef<HTMLImageElement>(null)
  const drawingCanvasRef = useRef<HTMLCanvasElement>(null)
  const eventOverlayRef = useRef<HTMLDivElement>(null)


  const handleMouseClick = (e: React.MouseEvent) => {
    const rect = e.currentTarget.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    const point: Point = { x, y }

    const ctx = drawingCanvasRef.current?.getContext('2d')
    if (!ctx) return

    ctx.strokeStyle = 'red'
    ctx.fillStyle = 'red'
    ctx.lineWidth = 2
    
    
    if (firstPoint && secondPoint) {
      // Already drew a rectangle
      // Reset rectangle and draw top left point
      setFirstPoint(point)
      setSecondPoint(null)
      
      // Reset drawing canvas
      ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)
    } else if (firstPoint) {
      // Only top left, draw second point and complete rectangle
      setSecondPoint(point)
      
      const bbox = calculateBoundingBox(firstPoint, point)
      if (!bbox) {
        console.log('Bruh')
        setFirstPoint(null)
        setSecondPoint(null)
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height)

        return
      }

      ctx.strokeRect(bbox.x, bbox.y, bbox.width, bbox.height)
      
      const normalizedBBox = normalizeBoundingBox(bbox)
      setBoundingBox(normalizedBBox)
    } else {
      // Neither points drawn yet, draw first point
      setFirstPoint(point)
    }
    
    // Draw circle at point
    ctx.beginPath()
    ctx.arc(x, y, 5, 0, 2 * Math.PI)
    ctx.fill()
  }

  const calculateBoundingBox = (p1: Point, p2: Point): BoundingBox | null => {
    const dx = p2.x - p1.x
    const dy = p2.y - p1.y

    if (dx == 0 || dy == 0) {
      return null
    }

    if (dx > 0 && dy > 0) {
      // p1 is top left, p2 is bottom right
      return {
        x: p1.x,
        y: p1.y,
        width: dx,
        height: dy
      }
    } else if (dx > 0 && dy < 0) {
      // p1 is bottom left, p2 is top right
      return {
        x: p1.x,
        y: p2.y,
        width: dx,
        height: -dy
      }
    } else if (dx < 0 && dy > 0) {
      // p1 is top right, p2 is bottom left
      return {
        x: p2.x,
        y: p1.y,
        width: -dx,
        height: dy
      }
    } else {
      // p1 is bottom right, p2 is top left
      return {
        x: p2.x,
        y: p2.y,
        width: -dx,
        height: -dy
      }
    }
  }

  const normalizeBoundingBox = (bbox: BoundingBox): BoundingBox | null => {
    if (!drawingCanvasRef.current) {
      return null
    }

    const canvasWidth = drawingCanvasRef.current.width
    const canvasHeight = drawingCanvasRef.current.height

    if (canvasWidth == 0 || canvasHeight == 0) {
      return null
    }

    return {
      x: bbox.x / canvasWidth,
      y: bbox.y / canvasHeight,
      width: bbox.width / canvasWidth,
      height: bbox.height / canvasHeight
    }
  }

  const handleConfirm = () => {
    console.log("Handle confirm called", boundingBox)
    if (boundingBox) {
      onConfirm(boundingBox)
    }
  }

  return (
    <div className="relative w-full">
      <img
        src={imageUrl}
        alt="Selectable"
        ref={imageRef}
        className="absolute top-0 left-0 w-full h-auto"
        onLoad={() => {
          const image = imageRef.current
          const canvas = drawingCanvasRef.current
          const overlay = eventOverlayRef.current
          if (image && canvas && overlay) {
            // Set canvas and overlay size to match image's rendered size
            const rect = image.getBoundingClientRect()
            canvas.width = rect.width
            canvas.height = rect.height
            console.log(rect.width, rect.height)
            canvas.style.width = rect.width + 'px'
            canvas.style.height = rect.height + 'px'

            overlay.style.width = rect.width + 'px'
            overlay.style.height = rect.height + 'px'
          } else {
            console.log("rip", image, canvas, overlay)
          }
        }}
      />
      <canvas
        ref={drawingCanvasRef}
        className="absolute top-0 left-0"
        style={{ pointerEvents: 'none' }}
      />
      <div
        className="absolute top-0 left-0"
        ref={eventOverlayRef}
        onClick={handleMouseClick}
      />
      {(
        <button
          // className="absolute bottom-4 left-1/2 transform -translate-x-1/2 px-4 py-1 bg-blue-600 text-white rounded"
          className='absolute px-4 py-1 bg-blue-600 text-white rounded'
          onClick={handleConfirm}
        >
          Confirm
        </button>
      )}
    </div>
  )
}

export default BoundingBoxSelector