export function SunIcon({className , color = "#fff"}) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      fill={color}
      viewBox="0 0 24 24"
      // width={size}
      // height={size}
      className={className}
    >
      <circle cx="12" cy="12" r="5" />
      <g>
        <line x1="12" y1="1" x2="12" y2="3" stroke={color} strokeWidth="2" />
        <line x1="12" y1="21" x2="12" y2="23" stroke={color} strokeWidth="2" />
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke={color} strokeWidth="2" />
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke={color} strokeWidth="2" />
        <line x1="1" y1="12" x2="3" y2="12" stroke={color} strokeWidth="2" />
        <line x1="21" y1="12" x2="23" y2="12" stroke={color} strokeWidth="2" />
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke={color} strokeWidth="2" />
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke={color} strokeWidth="2" />
      </g>
    </svg>
  );
}

  