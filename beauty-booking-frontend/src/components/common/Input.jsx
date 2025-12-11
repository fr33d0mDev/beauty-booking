/**
 * Input Component
 * Reusable input field with label and error handling
 */

const Input = ({
  label,
  type = 'text',
  name,
  value,
  onChange,
  onBlur,
  placeholder,
  error,
  required = false,
  disabled = false,
  className = '',
  icon: Icon,
  ...props
}) => {
  return (
    <div className={`w-full ${className}`}>
      {label && (
        <label htmlFor={name} className="block text-sm font-medium text-secondary-700 mb-1">
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </label>
      )}
      <div className="relative">
        {Icon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Icon className="h-5 w-5 text-secondary-400" />
          </div>
        )}
        <input
          type={type}
          id={name}
          name={name}
          value={value}
          onChange={onChange}
          onBlur={onBlur}
          placeholder={placeholder}
          disabled={disabled}
          className={`
            block w-full rounded-lg border
            ${Icon ? 'pl-10' : 'pl-3'} pr-3 py-2
            ${error ? 'border-red-500 focus:ring-red-500 focus:border-red-500' : 'border-secondary-300 focus:ring-primary-500 focus:border-primary-500'}
            ${disabled ? 'bg-secondary-100 cursor-not-allowed' : 'bg-white'}
            text-secondary-900 placeholder-secondary-400
            focus:outline-none focus:ring-2
            transition-smooth
          `}
          {...props}
        />
      </div>
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
};

export default Input;
