import React, { useState } from 'react';

function SearchBar(){
    const [value, setValue] = useState()
    const onChange = (e) => {
        setValue(e.target.value)

    }
    return (
        <div className="SearchBar">
            <div className="search">
                <div>
                    <input type="text" onChange={onChange} value={value} placeholder='Search'/>
                    
                </div>
            </div>
        </div>
    );
}

export default SearchBar;