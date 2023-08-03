import React from 'react';
import './Specs.css';
import Footer from '../footer/Footer.js';

function Specs() {
  return (

    <div className='all'>
      <div className='flexing'>
      <img className='image' src='https://tinyurl.com/23ljbjcl' alt='laptop' />


        <div className='kf'>
        <h3 className='card-heading'>KEY FEATURES</h3>
        <ul className='card-list'>
          <li>Model - HP EliteBook 8460p</li>
          <li>Processor - Intel Core i5</li>
          <li>Memory - 8GB DDR4</li>
          <li>Storage - 500 GB HDD</li>
          <li>Windows - Windows 10</li>
          <li>Microsoft Office installed</li>
        </ul>
        </div>
                
        <div className='m1'>
        <h3 className='card-heading'>MORE INFO</h3>
        <ul className='card-list'>
          <li>KU: HP246CL25684UNAFAMZ</li>
          <li>Production Country: USA</li>
          <li>Size (L x W x H cm): 33.8 x 23.7 x 1.89 cm</li>
          <li>Weight (kg): 2</li>
          <li>Main Material: PVC</li>
          <li>Care Label: Handle with care</li>
        </ul>
        <div>
        <button class="button-48" role="button"><span class="text">Order Now</span></button>

        </div>
        </div>
        </div>
        <div className='footer'>
      <Footer />
      </div>
    </div>
    
    
  );
}

export default Specs;