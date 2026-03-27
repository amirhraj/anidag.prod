import React from 'react';

const BookmarkIcon = ({ fill = '#000', className }) => {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill={fill}
      className={className}
    >
      <path d="M5 2C3.9 2 3 2.9 3 4V22L12 17L21 22V4C21 2.9 20.1 2 19 2H5Z" />
    </svg>
  );
};

export default BookmarkIcon;