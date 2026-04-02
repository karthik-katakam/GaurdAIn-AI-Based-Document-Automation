import '../Upload.css';
//Progress bar styles 
const ProgressBar = ({
    progress,
    color='blue', 
    height="16px"
}) => {
    //width attribute (Percentage/ inner progress bar ) is dynamically updated each second
    const progressStyle = {
        width: `${progress}%`, 
        backgroundColor: color, 
        height: height
    };

    return (
        <div className ="progress-bar-container">
            <div className='progress-bar' style={progressStyle}> </div>
        </div>
    )
};

export default ProgressBar