# -*- coding: utf-8 -*-
"""aspen simulation modelling.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VSAk4wpzyTCav07mHIvUwmiXfkfNVCcu
"""

import os
import win32com.client as win32
from typing import Literal

class Simulation:
    AspenSimulation = win32.gencache.EnsureDispatch("Apwn.Document")

    def __init__(self, AspenFileName: str, WorkingDirectoryPath: str, VISIBILITY: bool = True):
        print("The current Directory is :  ")
        print(os.getcwd())
        os.chdir(WorkingDirectoryPath)
        print("The new Directory where you should also have your Aspen file is : ")
        print(os.getcwd())
        self.AspenSimulation.InitFromArchive2(os.path.abspath(AspenFileName))
        print("The Aspen is active now. If you don't want to see Aspen open again, take VISIBILITY as False\n")
        self.AspenSimulation.Visible = VISIBILITY

    def CloseAspen(self):
        AspenFileName = self.Give_AspenDocumentName()
        print(AspenFileName)
        self.AspenSimulation.Close(os.path.abspath(AspenFileName))
        print("\nAspen should be closed now")

    @property
    def BLK(self):
        return self.AspenSimulation.Tree.Elements("Data").Elements("Blocks")

    @property
    def STRM(self):
        return self.AspenSimulation.Tree.Elements("Data").Elements("Streams")

    def BlockDelete(self, Blockname: str) -> None:
        self.BLK.Elements.Remove(Blockname)

    def BlockPlace(self, Blockname: str, EquipmentType: Literal["RCSTR", "RPlug", "DSTWU", "Flash2", "Mixer", "Heater", "Radfrac", "Splitter", "RYield"]) -> None:
        compositstring = Blockname + "!" + EquipmentType
        print(compositstring)
        self.BLK.Elements.Add(compositstring)

    def StreamPlace(self, Streamname: str, Streamtype: Literal["MATERIAL", "HEAT", ""]) -> None:
        compositstring = Streamname + "!" + Streamtype
        print(compositstring)
        self.STRM.Elements.Add(compositstring)

    def StreamDelete(self, Streamname: str) -> None:
        self.STRM.Elements.Remove(Streamname)

    def StreamConnect(self, Blockname: str, Streamname: str, Portname: str) -> None:
        self.BLK.Elements(Blockname).Elements("Ports").Elements(Portname).Elements.Add(Streamname)

    def StreamDisconnect(self, Blockname: str, Streamname: str, Portname: str) -> None:
        self.BLK.Elements(Blockname).Elements("Ports").Elements(Portname).Elements.Remove(Streamname)

    def StreamDeleteALL(self) -> None:
        self.STRM.RemoveAll()

    def BlockDeleteALL(self) -> None:
        self.BLK.RemoveAll()

    def VisibilityChange(self, VISIBILITY: bool) -> None:
        self.AspenSimulation.Visible = VISIBILITY

    def SheetCheckIfInputsAreComplete(self) -> bool:
        return self.AspenSimulation.COMPSTATUS

    def BlockCheckIfInputsAreComplete(self, Blockname: str) -> bool:
        return self.BLK.Elements(Blockname).COMPSTATUS

    def StreamCheckIfInputsAreComplete(self, Streamname: str) -> bool:
        return self.STRM.Elements(Streamname).COMPSTATUS

    def Give_AspenDocumentName(self) -> str:
        return self.AspenSimulation.FullName

    def DialogSuppression(self, TrueOrFalse: bool) -> None:
        self.AspenSimulation.SuppressDialogs = TrueOrFalse

    def EngineRun(self) -> None:
        self.AspenSimulation.Run2()

    def EngineStop(self) -> None:
        self.AspenSimulation.Stop()

    def EngineReinit(self) -> None:
        self.AspenSimulation.Reinit()

    def BlockReinit(self, Blockname: str) -> None:
        self.BLK.Elements(Blockname).Reinit()

    def StreamReinit(self, Streamname: str) -> None:
        self.STRM.Elements(Streamname).Reinit()

    def setup_hydrothermal_liquefaction(self):
        self.BlockPlace("Milling", "Mixer")
        self.BlockPlace("Grinding", "Mixer")
        self.BlockPlace("HTL_Reactor", "RCSTR")
        self.BlockPlace("Clump_Separator", "Splitter")
        self.StreamPlace("Feedstock", "MATERIAL")
        self.StreamPlace("Milled_Feedstock", "MATERIAL")
        self.StreamPlace("Ground_Feedstock", "MATERIAL")
        self.StreamPlace("Reacted_Product", "MATERIAL")
        self.StreamPlace("Separated_Clumps", "MATERIAL")
        self.StreamConnect("Milling", "Feedstock", "In")
        self.StreamConnect("Milling", "Milled_Feedstock", "Out")
        self.StreamConnect("Grinding", "Milled_Feedstock", "In")
        self.StreamConnect("Grinding", "Ground_Feedstock", "Out")
        self.StreamConnect("HTL_Reactor", "Ground_Feedstock", "In")
        self.StreamConnect("HTL_Reactor", "Reacted_Product", "Out")
        self.StreamConnect("Clump_Separator", "Reacted_Product", "In")
        self.StreamConnect("Clump_Separator", "Separated_Clumps", "Out")
        print("Hydrothermal liquefaction setup complete.")

    def setup_feedstock_collection(self):
        self.BlockPlace("GIS_Transport_Train", "Mixer")
        self.BlockPlace("GIS_Transport_Road", "Mixer")
        self.BlockPlace("Labor_Cost", "RYield")
        self.BlockPlace("Fixed_Costs", "RYield")
        self.BlockPlace("Operating_Costs", "RYield")
        self.StreamPlace("Collected_Feedstock_Train", "MATERIAL")
        self.StreamPlace("Collected_Feedstock_Road", "MATERIAL")
        self.StreamPlace("Feedstock_to_Plant", "MATERIAL")
        self.StreamPlace("Labor_Cost_Stream", "MATERIAL")
        self.StreamPlace("Fixed_Cost_Stream", "MATERIAL")
        self.StreamPlace("Operating_Cost_Stream", "MATERIAL")
        self.StreamConnect("GIS_Transport_Train", "Collected_Feedstock_Train", "In")
        self.StreamConnect("GIS_Transport_Train", "Feedstock_to_Plant", "Out")
        self.StreamConnect("GIS_Transport_Road", "Collected_Feedstock_Road", "In")
        self.StreamConnect("GIS_Transport_Road", "Feedstock_to_Plant", "Out")
        self.StreamConnect("Labor_Cost", "Labor_Cost_Stream", "In")
        self.StreamConnect("Fixed_Costs", "Fixed_Cost_Stream", "In")
        self.StreamConnect("Operating_Costs", "Operating_Cost_Stream", "In")
        print("Feedstock collection setup complete.")

sim = Simulation("example_file.bkp", "C:\\Path\\To\\Aspen\\Files", VISIBILITY=True)
sim.setup_hydrothermal_liquefaction()
sim.setup_feedstock_collection()
sim.CloseAspen()