import { useCallback, useState } from "react";




const ErrorBoundaryImage = ({src, defaultSrc, alt}) =>{

    const [currentSrc, setCurrentSrc] = useState(src);

      const handleError = () => {
        setCurrentSrc(defaultSrc);
        e.target.onerror = null;
      };

    return(
        <img src={currentSrc} alt={alt} onError={handleError} loading="lazy"  width={70} height={90}  />
    )
}

export default   ErrorBoundaryImage