
interface CaptureButtonProps {
  handleClick: () => void
}

const CaptureButton = ({ handleClick }: CaptureButtonProps) => {
  
  return (
    <button
      type="button"
      aria-label="Capture photo"
      onClick={handleClick}
      className={`
        relative grid place-items-center
        w-16 h-16
        rounded-full
        bg-white/90
        shadow-lg
        ring-2 ring-white/80
        hover:bg-white active:scale-95
        transition
        disabled:opacity-50 disabled:cursor-not-allowed
        absolute left-1/2 -translate-x-1/2 bottom-24
      `}
    >
      {/* Inner “shutter” circle */}
      <span className="block w-12 h-12 rounded-full bg-white ring-2 ring-gray-300" />
    </button>
  )
}

export default CaptureButton