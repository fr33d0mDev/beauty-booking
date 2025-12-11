/**
 * Card Component
 * Reusable card container with optional hover effect
 */

const Card = ({
  children,
  className = '',
  hover = false,
  onClick,
  padding = 'md',
}) => {
  const baseStyles = 'bg-white rounded-lg border border-secondary-200 transition-smooth';
  const hoverStyles = hover ? 'card-shadow cursor-pointer hover:border-primary-300' : 'shadow-sm';

  const paddingStyles = {
    none: '',
    sm: 'p-3',
    md: 'p-4',
    lg: 'p-6',
    xl: 'p-8',
  };

  return (
    <div
      onClick={onClick}
      className={`${baseStyles} ${hoverStyles} ${paddingStyles[padding]} ${className}`}
    >
      {children}
    </div>
  );
};

export default Card;
