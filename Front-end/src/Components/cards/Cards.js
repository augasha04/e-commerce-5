// import React, { useEffect, useState } from 'react'
// import './Cards.css'

// function Cards() {
//   const [products, setProducts] = useState([])
//   useEffect (() => {
//     fetch('http://localhost:3001/products')
//     .then(res => {
//       return res.json()
//     }).then(data => {
//       setProducts(data)
//     });
//   },[])
  
//   return (
//     <div className="services-container">
//       {products.map((product) =>(
//         <div className="service-card" key={product.id}>
//           <img className="service-image" src={product.image_url} alt='product'/>
//           <h4>{product.name}</h4>
//           <p>USD {product.price}</p>
//           <button className='btn'>Buy Now</button>
//         </div>
//       ))}

//     </div>
//   )
// }

// export default Cards

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom
import './Cards.css';

function Cards() {
  const [products, setProducts] = useState([]);
  useEffect(() => {
    fetch('http://localhost:3001/products')
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        setProducts(data);
      });
  }, []);

  return (
    <div className="services-container">
      {products.map((product) => (
        <div className="service-card" key={product.id}>
          <img className="service-image" src={product.image_url} alt="product" />
          <h4>{product.name}</h4>
          <p>USD {product.price}</p>
          <Link to={`/products/${product.id}`}> {/* Use Link to navigate to the product page */}
            <button className="btn">Buy Now</button>
          </Link>
        </div>
      ))}
    </div>
  );
}

export default Cards;
