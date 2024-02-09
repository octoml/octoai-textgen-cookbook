const LoadingDots = () => {
  return (
    <div role="status" id="loading-dots">
      <span className="sr-only">Loading...</span>
      <div className="dot"></div>
      <div className="dot"></div>
      <div className="dot"></div>
    </div>
  );
};

export default LoadingDots;
