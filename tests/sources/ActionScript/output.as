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

  private var memoryLog = new Array()
  private var memoryMax = 0
  private var memoryMin = 0
  private var memoryColor
  private var ticks = 0
  private var frameRate = 0
  private var cpuLog = new Array()
  private var cpuMax = 0
  private var cpuMin = 0
  private var cpuColor
  private var cpu
  private var lastUpdate = 0
  private var sampleSize = 30
  private var graphHeight
  private var graphWidth

  private var fireParticles = new Array()
  private var fireMC = new MovieClip()
  private var palette = new Array()
  private var anchors = new Array()
  private var frame

  public function Flames () {
    addChildAt(fireMC, 1)
    frame = new Rectangle(2, 2, stage.stageWidth - 2, stage.stageHeight - 2)

    var colWidth = Math.floor(frame.width / 10)
    for (var i = 0; i < 10; i++) {
      anchors[i] = Math.floor(i * colWidth)
    }

    setPalette()

    frameRate = stage.frameRate

    addEventListener(Event.ENTER_FRAME, drawParticles)
    addEventListener(Event.ENTER_FRAME, getStats)
    addEventListener(Event.ENTER_FRAME, drawGraph)
  }

  private function setPalette () {
    var black = 0x000000
    var blue = 0x0000FF
    var red = 0xFF0000
    var orange = 0xFF7F00
    var yellow = 0xFFFF00
    var white = 0xFFFFFF
  }

  private function getColorRange (color1, color2, steps) {
    var output = new Array()
    for (var i = 0; i < steps; i++) {
      var progress = i / steps
      var color = Color.interpolateColor(color1, color2, progress)
      output.push(color)
    }
    return output
  }

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
          size *= 1.2
        } else {
          transperency = 0.1
          size *= 0.3
          particle.x += Math.floor(Math.random() * 4 - 2)
        }
      }

      fireMC.graphics.lineStyle(5, color, 0.1)
      fireMC.graphics.beginFill(color, transperency)
      fireMC.graphics.drawCircle(particle.x, particle.y, size)
      fireMC.graphics.endFill()
      particle.life--
    }
  }

  private function createParticles (count) {
    var anchorPoint = 0
    for (var i = 0; i < count; i++) {
      var particle = new Object()
      particle.x = Math.floor(Math.random() * frame.width / 10) + anchors[anchorPoint]
      particle.life = 70 + Math.floor(Math.random() * 30)

      particle.anchor = anchors[anchorPoint] + Math.floor(Math.random() * 5)

      anchorPoint = (anchorPoint == 9) ? 0 : anchorPoint + 1
    }
  }

}
}