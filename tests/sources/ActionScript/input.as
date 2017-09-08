/*
* SOURCE:
* https://code.tutsplus.com/tutorials/actionscript-30-optimization-a-practical-example--active-11295
* */

package com.pjtops {

import flash.display.MovieClip;
import flash.events.Event;

import fl.motion.Color;

import flash.geom.Point;
import flash.geom.Rectangle;
import flash.text.TextField;
import flash.system.System;
import flash.utils.getTimer;

public class Flames extends MovieClip {

  private var memoryLog = new Array() // stores System.totalMemory values for display in the graph
  private var memoryMax = 0 // the highest value of System.totalMemory recorded so far
  private var memoryMin = 0  // the lowest value of System.totalMemory recorded so far
  private var memoryColor // the color used by text displaying memory info

  private var ticks = 0 // counts the number of times getStats() is called before the next frame rate value is set
  private var frameRate = 0  //the original frame rate value as set in Adobe Flash
  private var cpuLog = new Array() // stores cpu values for display in the graph
  private var cpuMax = 0 // the highest cpu value recorded so far
  private var cpuMin = 0 // the lowest cpu value recorded so far
  private var cpuColor   // the color used by text displaying cpu
  private var cpu // the current calculated cpu use

  private var lastUpdate = 0 // the last time the framerate was calculated
  private var sampleSize = 30 // the length of memoryLog & cpuLog
  private var graphHeight
  private var graphWidth

  private var fireParticles = new Array() // stores all active flame particles
  private var fireMC = new MovieClip() // the canvas for drawing the flames
  private var palette = new Array() // stores all available colors for the flame particles
  private var anchors = new Array() // stores horizontal points along fireMC which act like magnets to the particles
  private var frame // the movieclips bounding box

  // class constructor. Set up all the events, timers and objects
  public function Flames () {
    addChildAt(fireMC, 1)
    frame = new Rectangle(2, 2, stage.stageWidth - 2, stage.stageHeight - 2)

    var colWidth = Math.floor(frame.width / 10)
    for (var i = 0; i < 10; i++) {
      anchors[i] = Math.floor(i * colWidth)
    }

    setPalette()

    /*
    memoryColor = memoryTF.textColor
    cpuColor = cpuTF.textColor
    graphHeight = graphMC.height
    graphWidth = graphMC.width
    */

    frameRate = stage.frameRate

    addEventListener(Event.ENTER_FRAME, drawParticles)
    addEventListener(Event.ENTER_FRAME, getStats)
    addEventListener(Event.ENTER_FRAME, drawGraph)
  }

  //creates a collection of colors for the flame particles, and stores them in palette
  private function setPalette () {
    var black = 0x000000
    var blue = 0x0000FF
    var red = 0xFF0000
    var orange = 0xFF7F00
    var yellow = 0xFFFF00
    var white = 0xFFFFFF

    /*
    palette = palette.concat(getColorRange(black, blue, 10))
    palette = palette.concat(getColorRange(blue, red, 30))
    palette = palette.concat(getColorRange(red, orange, 20))
    palette = palette.concat(getColorRange(orange, yellow, 20))
    palette = palette.concat(getColorRange(yellow, white, 20))
    */
  }

//returns a collection of colors, made from different mixes of color1 and color2
  private function getColorRange (color1, color2, steps) {
    var output = new Array()
    for (var i = 0; i < steps; i++) {
      var progress = i / steps
      var color = Color.interpolateColor(color1, color2, progress)
      output.push(color)
    }
    return output
  }

// calculates statistics for the current state of the application, in terms of memory used and the cpu %
  private function getStats (event) {
    ticks++
    var now = getTimer()

    if (now - lastUpdate < 1000) {
      return
    } else {
      lastUpdate = now
    }

    cpu = 100 - ticks / frameRate * 100
    cpuLog.push(cpu)
    ticks = 0
    cpuTF.text = cpu.toFixed(1) + '%'
    if (cpu > cpuMax) {
      cpuMax = cpu
      cpuMaxTF.text = cpuTF.text
    }
    if (cpu < cpuMin || cpuMin == 0) {
      cpuMin = cpu
      cpuMinTF.text = cpuTF.text
    }

    var memory = System.totalMemory / 1000000
    memoryLog.push(memory)
    memoryTF.text = String(memory.toFixed(1)) + 'mb'
    if (memory > memoryMax) {
      memoryMax = memory
      memoryMaxTF.text = memoryTF.text
    }
    if (memory < memoryMin || memoryMin == 0) {
      memoryMin = memory
      memoryMinTF.text = memoryTF.text
    }
  }

  /*
  //render's a graph on screen, that shows trends in the applications frame rate and memory consumption
  private function drawGraph (event) {
  graphMC.graphics.clear()
  var ypoint, xpoint
  var logSize = memoryLog.length

  if (logSize > sampleSize) {
    memoryLog.shift()
    cpuLog.shift()
    logSize = sampleSize
  }
  var widthRatio = graphMC.width / logSize

  graphMC.graphics.lineStyle(3, memoryColor, 0.9)
  var memoryRange = memoryMax - memoryMin
  for (var i = 0; i < memoryLog.length; i++) {
    ypoint = ( memoryLog[i] - memoryMin ) / memoryRange * graphHeight
    xpoint = (i / sampleSize) * graphWidth
    if (i == 0) {
      graphMC.graphics.moveTo(xpoint, -ypoint)
      continue
    }
    graphMC.graphics.lineTo(xpoint, -ypoint)
  }

  graphMC.graphics.lineStyle(3, cpuColor, 0.9)
  for (var j = 0; j < cpuLog.length; j++) {
    ypoint = cpuLog[j] / 100 * graphHeight
    xpoint = ( j / sampleSize ) * graphWidth
    if (j == 0) {
      graphMC.graphics.moveTo(xpoint, -ypoint)
      continue
    }
    graphMC.graphics.lineTo(xpoint, -ypoint)
  }
  }
  */

//renders each flame particle and updates it's values
  private function drawParticles (event) {
    createParticles(20)

    fireMC.graphics.clear()
    for (var i in fireParticles) {
      var particle = fireParticles[i]

      if (particle.life == 0) {
        delete( fireParticles[i] )
        continue
      }

      var size = Math.floor(particle.size * particle.life / 100)
      var color = palette[particle.life]
      var transperency = 0.3

      if (size < 3) {
        size *= 3
        color = 0x333333
        particle.x += Math.random() * 8 - 4
        particle.y -= 2
        transperency = 0.2
      } else {
        particle.y = frame.bottom - ( 100 - particle.life )

        if (particle.life > 90) {
          size *= 1.5
        } else if (particle.life > 45) {
          /* particle.x += Math.floor(Math.random() * 6 - 3)*/
          size *= 1.2
          /* // */
        } else {
          transperency = 0.1 // /*
          size *= 0.3
          particle.x += Math.floor(Math.random() * 4 - 2) // */
        }
      }

      fireMC.graphics.lineStyle(5, color, 0.1)
      fireMC.graphics.beginFill(color, transperency)
      fireMC.graphics.drawCircle(particle.x, particle.y, size)
      fireMC.graphics.endFill()
      particle.life--
    }
  }

//generates flame particle objects
  private function createParticles (count) {
    var anchorPoint = 0
    for (var i = 0; i < count; i++) {
      var particle = new Object()
      particle.x = Math.floor(Math.random() * frame.width / 10) + anchors[anchorPoint]
      // particle.y = frame.bottom
      particle.life = 70 + Math.floor(Math.random() * 30)
      // particle.size = 5 + Math.floor(Math.random() * 10)
      // fireParticles.push(particle)

      // if (particle.size > 12) {
      //   particle.size = 10
      // }
      particle.anchor = anchors[anchorPoint] + Math.floor(Math.random() * 5)

      anchorPoint = (anchorPoint == 9) ? 0 : anchorPoint + 1
    }
  }

}
}