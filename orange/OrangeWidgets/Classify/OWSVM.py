"""
<name>Support Vector Machines</name>
<description>Support Vector Machines learner/classifier.</description>
<icon>icons/BasicSVM.png</icon>
<contact>Ales Erjavec (ales.erjavec(@at@)fri.uni-lj.si)</contact> 
<priority>110</priority>
"""

import orange, orngSVM, OWGUI
from OWWidget import *

class OWSVM(OWWidget):
    settingsList=["C","nu","p","probability","shrinking","gamma","degree", "coef0", "kernel_type", "name", "useNu"]
    def __init__(self, parent=None, signalManager=None, name="SVM"):
        OWWidget.__init__(self, parent, signalManager, name)
        self.inputs=[("Example Table", ExampleTable, self.cdata)]
        self.outputs=[("Learner", orange.Learner),("Classifier", orange.Classifier),("Support Vectors", ExampleTable)]

        self.kernel_type = 2
        self.gamma = 0.5
        self.coef0 = 0.0
        self.degree = 3
        self.C = 1.0
        self.p = 0.5
        self.eps = 1e-3
        self.nu = 0.5
        self.shrinking = 1
        self.probability=0
        self.useNu=0
        self.data = None
        self.name="SVM Learner/Classifier"
        
        OWGUI.lineEdit(self.controlArea, self, "name")
        b=QVButtonGroup("Kernel", self.controlArea)
        self.kernelradio = OWGUI.radioButtonsInBox(b, self, "kernel_type", btnLabels=["Linear,   x.y", "Polynomial,   (g*x.y+c)^d",
                    "RBF,   exp(-g*(x-y).(x-y))", "Sigmoid,   tanh(g*x.y+c)"], callback=self.changeKernel)

        self.gcd = OWGUI.widgetBox(b, orientation="horizontal")
        self.leg = OWGUI.doubleSpin(self.gcd, self, "gamma",0.0,10.0,0.25, label="g: ", orientation="horizontal", callback=self.changeKernel)
        self.led = OWGUI.doubleSpin(self.gcd, self, "coef0", 0.0,10.0,0.5, label="  c: ", orientation="horizontal", callback=self.changeKernel)
        self.lec = OWGUI.doubleSpin(self.gcd, self, "degree", 0.0,10.0,0.5, label="  d: ", orientation="horizontal", callback=self.changeKernel)
        b=OWGUI.widgetBox(self.controlArea, self, "Options")
        OWGUI.doubleSpin(b,self, "C", 0.0, 100.0, 0.5, label="Model complexity (C)", orientation="horizontal")
        OWGUI.doubleSpin(b,self, "p", 0.0, 10.0, 0.1, label="Tolerance (p)", orientation="horizontal")
        OWGUI.doubleSpin(b,self, "eps", 0.0, 0.5, 0.001, label="Numeric precision (eps)", orientation="horizontal")

        OWGUI.checkBox(b,self, "shrinking", label="Shrinking")
        OWGUI.checkBox(b,self, "useNu", label="Limit the number of support vectors", callback=lambda:self.nuBox.setDisabled(not self.useNu))
        self.nuBox=OWGUI.doubleSpin(b,self, "nu", 0.0,1.0,0.1, label="Complexity bound (nu)", orientation="horizontal")

        OWGUI.button(b,self,"&Apply settings", callback=self.applySettings)
        self.nuBox.setDisabled(not self.useNu)
        self.resize(100,100)        
        self.loadSettings()
        self.changeKernel()

        
    def changeKernel(self):
        if self.kernel_type==0:
            for a,b in zip([self.leg, self.led, self.lec], [1,1,1]):
                a.setDisabled(b)
        elif self.kernel_type==1:
            for a,b in zip([self.leg, self.led, self.lec], [0,0,0]):
                a.setDisabled(b)
        elif self.kernel_type==2:
            for a,b in zip([self.leg, self.led, self.lec], [0,1,1]):
                a.setDisabled(b)
        elif self.kernel_type==3:
            for a,b in zip([self.leg, self.led, self.lec], [0,0,1]):
                a.setDisabled(b)

    def cdata(self, data=None):
        if data:
            self.data=data
        else:
            self.data=None
        self.applySettings()

    def applySettings(self):
        self.learner=orngSVM.SVMLearner()
        for attr in ("name", "kernel_type", "degree", "shrinking"):
            setattr(self.learner, attr, getattr(self, attr))

        for attr in ("gamma", "coef0", "C", "p", "eps", "nu"):
            setattr(self.learner, attr, float(getattr(self, attr)))

        self.learner.svm_type=0
        
        if self.useNu:
            self.learner.svm_type=1

        self.classifier=None
        self.supportVectors=None
        if self.data:
            if self.data.domain.classVar.varType==orange.VarTypes.Continuous:
                self.learner.svm_type+=3
            self.classifier=self.learner(self.data)
            self.supportVectors=self.classifier.supportVectors
            self.classifier.name=self.name
        self.send("Learner", self.learner)
        self.send("Classifier", self.classifier)
        self.send("Support Vectors", self.supportVectors)

import sys
if __name__=="__main__":
    app=QApplication(sys.argv)
    w=OWSVM()
    app.setMainWidget(w)
    w.show()
    d=orange.ExampleTable("../../doc/datasets/housing.tab")
    w.cdata(d)
    app.exec_loop()
    w.saveSettings()
