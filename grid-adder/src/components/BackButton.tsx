
interface BackButtonProps {
  handleClick: () => void
}

const BackButton = ({ handleClick }: BackButtonProps) => {

  return (
    <div className="absolute top-4 left-4 bg-black/50 backdrop-blur-sm rounded-lg">
      <button
        onClick={handleClick}
        className="bg-black/30 text-white px-6 py-4 rounded-lg hover:bg-black/70">
          ◀ Back
      </button>
    </div>
  )
}

export default BackButton