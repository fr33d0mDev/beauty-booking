/**
 * Loading Component
 * Loading spinner with optional text
 */

const Loading = ({ text = 'Loading...', fullScreen = false, size = 'md' }) => {
  const sizes = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12',
    lg: 'w-16 h-16',
  };

  const content = (
    <div className="flex flex-col items-center justify-center gap-3">
      <div className={`spinner ${sizes[size]}`}></div>
      {text && <p className="text-secondary-600 font-medium">{text}</p>}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="fixed inset-0 bg-white bg-opacity-90 flex items-center justify-center z-50">
        {content}
      </div>
    );
  }

  return content;
};

export default Loading;
