
import modalStyles from './modal.module.css'

const Modal = ({activeModal, setActiveModal, children}) =>{
    return(
        <>
        <div className={`${modalStyles.modal} ${activeModal ? modalStyles.active : ''}`} onClick={()=> setActiveModal(false)}>
            <div className={`${modalStyles.modal_content} ${activeModal ? modalStyles.active : ''}`} onClick={e => e.stopPropagation()}>
                    {children}
                    
            </div>
        </div>
        </>
    )
}
export default Modal