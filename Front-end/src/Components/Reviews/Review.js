// import React, { useState } from 'react';
// import './review.css'

// const Review = () => {
//   const [reviews, setReviews] = useState([]);
//   const [newReview, setNewReview] = useState({ name: '', comment: '' });

//   const handleInputChange = (event) => {
//     const { name, value } = event.target;
//     setNewReview({ ...newReview, [name]: value });
//   };

//   const handleSubmit = (event) => {
//     event.preventDefault();
//     if (newReview.name.trim() === '' || newReview.comment.trim() === '') {
//       return; // Prevent submitting empty reviews
//     }

//     // Add the new review to the reviews list
//     setReviews([...reviews, newReview]);

//     // Clear the input fields
//     setNewReview({ name: '', comment: '' });
//   };

//   return (
//     <div>
//       <h2>Reviews</h2>
//       {reviews.length === 0 ? (
//         <p>No reviews yet.</p>
//       ) : (
//         <ul>
//           {reviews.map((review, index) => (
//             <li key={index}>
//               <strong>{review.name}:</strong> {review.comment}
//             </li>
//           ))}
//         </ul>
//       )}
//       <form onSubmit={handleSubmit}>
//         <div>
//           <label htmlFor="name">Name:</label>
//           <input
//             type="text"
//             id="name"
//             name="name"
//             value={newReview.name}
//             onChange={handleInputChange}
//           />
//         </div>
//         <div>
//           <label htmlFor="comment">Comment:</label>
//           <textarea
//             id="comment"
//             name="comment"
//             value={newReview.comment}
//             onChange={handleInputChange}
//           />
//         </div>
//         <button type="submit">Submit Review</button>
//       </form>
//     </div>
//   );
// };

// export default Review;

import React, { useState } from 'react';
import './review.css'; // Import the CSS file

const Review = () => {
  const [reviews, setReviews] = useState([]);
  const [newReview, setNewReview] = useState({ name: '', comment: '' });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setNewReview({ ...newReview, [name]: value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (newReview.name.trim() === '' || newReview.comment.trim() === '') {
      return; // Prevent submitting empty reviews
    }

    // Add the new review to the reviews list
    setReviews([...reviews, newReview]);

    // Clear the input fields
    setNewReview({ name: '', comment: '' });
  };

  return (
    <div className="review-container">
      <div className="review-title">Reviews</div>
      {reviews.length === 0 ? (
        <p>No reviews yet.</p>
      ) : (
        <ul className="review-list">
          {reviews.map((review, index) => (
            <li key={index}>
              <strong>{review.name}:</strong> {review.comment}
            </li>
          ))}
        </ul>
      )}
      <form className="review-form" onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={newReview.name}
            onChange={handleInputChange}
          />
        </div>
        <div>
          <label htmlFor="comment">Comment:</label>
          <textarea
            id="comment"
            name="comment"
            value={newReview.comment}
            onChange={handleInputChange}
          />
        </div>
        <button type="submit">Submit Review</button>
      </form>
    </div>
  );
};

export default Review;
