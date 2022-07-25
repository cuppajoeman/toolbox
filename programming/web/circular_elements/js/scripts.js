document.querySelectorAll( '.circlegraph' ).forEach( ( circlegraph )=>{
    let circles = circlegraph.querySelectorAll( '.circle' )
    let theta =0, dtheta = Math.PI * 2 / circles.length
    for( let i = 0; i < circles.length; ++i ){
          let circle = circles[i]
          theta += dtheta
          circle.style.transform = `rotate(${theta}rad) translate(${circlegraph.clientWidth / 2}px) rotate(-${theta}rad)`
        }
})
