


var p2 = window.prompt('Enter Player 2 Name:')
if (p1 == '') {
  p1 = 'Player 1'
}
if (p2 == '') {
  p2 = 'Player 2'
}


var counter = 0






function xC (bl) {
  var a1 = document.getElementById(bl)
  
  
  
  else {
    a1.style.color = 'blue'
  }
}

function B_press (b_d) {
  var t = document.getElementById('turn')
  var c = document.getElementById(b_d)
  c.innerHTML = ss
  result[b_d] = ss
  c.disabled = true
  xC(b_d)
  if (ss == 'X') {
    ss = 'O'
  }
  else {
    
  }
  if (counter > 3) {
    Win()
  }
  
  
  
  
  
  
  
}

function arr () {
  for (i = 0; i <= 9; i++) {
    result[i] = null
  }
  counter = 0
}

function col (x, y, z) {
  var a1 = document.getElementById(x) 
  var c1 = document.getElementById(z) 
  
}

function Win () {
  if (result[0] == result[1] && result[0] == result[2]) {
    if (result[0] != null) {
      
      
      
      col(a, b, c)
      if (result[0] == 'X') {
        alert(p1 + ' Wins ')
      }
      else {
        alert(p2 + ' Wins ')
      }
      dis()
      b()
    }
  }
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  if (result[6] == result[7] && result[6] == result[8]) {
    if (result[6] != null) {
      var a = 6
      var b = 7
      var c = 8
      col(a, b, c)
      if (result[6] == 'X') {
        alert(p1 + ' Wins ')
      }
      else {
        alert(p2 + ' Wins ')
      }
      dis()
      b()
    }
  }
  if (result[0] == result[3] && result[0] == result[6]) {
    if (result[0] != null) {
      var a = 0
      var b = 3
      var c = 6
      col(a, b, c)
      if (result[0] == 'X') {
        alert(p1 + ' Wins ')
      }
      else {
        alert(p2 + ' Wins ')
      }
    }
    dis()
    b()
  }
  if (result[1] == result[4] && result[1] == result[7]) {
    if (result[1] != null) {
      var a = 1
      var b = 4
      var c = 7
      col(a, b, c)
      if (result[1] == 'X') {
        alert(result[1] + ' Wins ')
      }
      else {
        alert(p2 + ' Wins ')
      }
      dis()
      b()
    }
  }
  if (result[2] == result[5] && result[2] == result[8]) {
    if (result[2] != null) {
      var a = 2
      var b = 5
      var c = 8
      col(a, b, c)
      if (result[2] == 'X') {
        alert(p1 + ' Wins ')
      }
      else {
        alert(p2 + ' Wins ')
      }
      dis()
      b()
    }
  }
  if (result[0] == result[4] && result[0] == result[8]) {
    
  }
  if (result[2] == result[4] && result[2] == result[6]) {
    if (result[2] != null) {
      var a = 2
      var b = 4
      var c = 6
      col(a, b, c)
      if (result[2] == 'X') {
        alert(result[2] + ' Wins ')
      }
      else {
        alert(p2 + ' Wins ')
      }
      dis()
      b()
    }
  }
  if (counter == 8) {
    alert('MATCH DRAW')
    b()
  }
}

function T () {
  var v = 0
  ss = 'X'
  var tbody = '<table border=\'5px\' width=\'300px\' height=\'300px\'>'
  for (i = 0; i < 3; i++) {
    tbody += '<tr>'
    for (j = 0; j < 3; j++) {
      var b_id = v
      tbody += '<td><button id=\'' + b_id + '\' onclick=\'B_press("' + b_id + '")\'></button></td>'
      v++
    }
    tbody += '</tr>'
  }

  tbody += '</table>'
  var o = document.getElementById('tb')
  o.innerHTML = tbody
  arr()
  alert(p1 + ' turn')
}

document.write('<h2 class=\'player1\'>Player 1 = ' + p1 + '</h2>')
document.write('<h2 class=\'player2\'>Player 2 = ' + p2 + '</h2>') 
    