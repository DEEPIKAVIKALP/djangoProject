function onRemove(id){
        cart_id=id.replace(/\D/g,'');
        //window.alert(cart_id)
        a=""
        a=cart_id+""
        location.href=a
        // /cart/1
    }
function AddValue(id)
    { 
      //window.alert("hello");
      cart_id=id.replace(/\D/g,'');
      //window.alert(cart_id);
      quant_id="quantity_id"+cart_id;
      
      totalprice_id="total_id"+cart_id;
      
      pri_id="price_id"+cart_id;
      //window.alert(pri_id+totalprice_id+quant_id);
      
      prev_qant = parseInt(document.getElementById(quant_id).value);
      

      document.getElementById(quant_id).value=parseInt(document.getElementById(quant_id).value)+1;
      document.getElementById(quant_id).innerHTML=document.getElementById(quant_id).value;
      
      valu= parseInt(document.getElementById(quant_id).value) * parseFloat(document.getElementById(pri_id).textContent);
      document.getElementById(totalprice_id).textContent = valu;
      //window.alert(valu);
      new_valu = parseInt((document.getElementById(quant_id).value)-prev_qant) * parseFloat(document.getElementById(pri_id).textContent);
      
      document.getElementById("Stotal").textContent = parseInt(document.getElementById("Stotal").textContent) + new_valu;


    
  }
function SubtractValue(id)
  { cart_id=id.replace(/\D/g,'');
    quant_id="quantity_id"+cart_id;
    totalprice_id="total_id"+cart_id;
    pri_id="price_id"+cart_id;
    prev_qant = parseInt(document.getElementById(quant_id).value);
    if(parseInt(document.getElementById(quant_id).value)>0)
    document.getElementById(quant_id).value=parseInt(document.getElementById(quant_id).value)-1;
    else
      document.getElementById("message").innerHTML="Cant be less than 0"
    document.getElementById(quant_id).innerHTML=document.getElementById(quant_id).value;
    valu= parseInt(document.getElementById(quant_id).value) * parseFloat(document.getElementById(pri_id).textContent);
    document.getElementById(totalprice_id).textContent = valu;

    new_valu = parseInt((document.getElementById(quant_id).value)-prev_qant) * parseFloat(document.getElementById(pri_id).textContent);
      
      document.getElementById("Stotal").textContent = parseInt(document.getElementById("Stotal").textContent) + new_valu;
  }
  