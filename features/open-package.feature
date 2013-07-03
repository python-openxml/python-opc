Feature: Open an OPC package
  In order to access the methods and properties on an OPC package
  As an Open XML developer
  I need to open an arbitrary package

  Scenario: Open a PowerPoint file
     Given a python-opc working environment
      When I open a PowerPoint file
      Then the expected package rels are loaded
       And the expected parts are loaded
