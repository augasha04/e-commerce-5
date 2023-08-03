import ViewProducts from "./ViewProducts";
import { useEffect, useState } from "react";
import './allproducts.css'

function SellerProducts(){
    const[allproducts, setProducts]=useState([])
    const[choosen_category, setCategory]= useState('All')
    const [searchLenght, setSearchLenght] = useState(0)
    const [lookingFor, setLook] = useState('')
    useEffect(()=>{
        fetch('http://localhost:5000/products')
        .then((r)=>r.json())
        .then((data)=>{
            setProducts(data)
        })        
    }, [])

    
    function handleSearch(e){
        let word = e.target.value
        setLook(word)        
        setSearchLenght(word.length)
    }
    let search = allproducts.filter((product)=>{
        if(product.name.slice(0,searchLenght).toLowerCase() == lookingFor.toLowerCase()){
            return product
        }
        else if(searchLenght == 0){
            return allproducts
        }
    })
   
    let filtered_products = search.filter((product)=>{
        if(product.category == choosen_category){
            return product
        }
        else if(choosen_category == 'All'){
            return search
        }
    })
    let categories = ['All','Televisions' , 'Laptops', 'Smartphones', 'Tablets', 'Cameras']
    return(
        <div className="allproducts-container">
            <div>
            <input
            type="search"
            placeholder="Search product by name"
            onChange={handleSearch} 
            />
            </div>
            <div className="button-arrangement">
                {
                    categories.map((category)=>{
                        return(
                            <button 
                            className="button-85"
                            id={category}
                             key={category}
                             onClick={(e)=>{
                                setCategory(e.target.id)
                             }}
                             >{category}</button>
                        )
                    })
                }
            </div>                    
            <ViewProducts shop_products={filtered_products} searchValue={searchLenght} currentCategory={choosen_category}/>
        </div>
    )
}
 export default SellerProducts;