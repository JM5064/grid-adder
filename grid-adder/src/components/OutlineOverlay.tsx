

const OutlineOverlay = () => {
  const padding =10

  return (
    <div
      className={`absolute top-0 left-0 w-full h-full object-cover pointer-events-none`}
    >
      <div
        style={{
          position: "absolute",
          top: padding,
          left: padding,
          right: padding,
          bottom: padding,
          border: `6px dashed black`,
          borderRadius: 10,
        }}
      />
    </div>
  );
}

export default OutlineOverlay