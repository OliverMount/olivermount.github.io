from neuron import h
from neuron.units import ms, mV, µm 

import matplotlib.pyplot as plt   # For plotting using matplotlib
from matplotlib.lines import Line2D  # Import Line2D for custom legend entries

h.load_file("stdrun.hoc") #load the standard run library to give us high-level simulation control functions (e.g. running a simulation for a given period of time):


class BallAndStick:
    def __init__(self, gid):
        self._gid = gid
        self._setup_morphology()
        self._setup_biophysics()

    def _setup_morphology(self):
        self.soma = h.Section(name="soma", cell=self)
        self.dend = h.Section(name="dend", cell=self)
        self.dend.connect(self.soma)
        self.all = self.soma.wholetree()
        self.soma.L = self.soma.diam = 12.6157 * µm
        self.dend.L = 200 * µm
        self.dend.diam = 1 * µm

    def _setup_biophysics(self):
        for sec in self.all:
            sec.Ra = 100  # Axial resistance in Ohm * cm
            sec.cm = 1  # Membrane capacitance in micro Farads / cm^2
        self.soma.insert("hh")
        for seg in self.soma:
            seg.hh.gnabar = 0.12  # Sodium conductance in S/cm2
            seg.hh.gkbar = 0.036  # Potassium conductance in S/cm2
            seg.hh.gl = 0.0003  # Leak conductance in S/cm2
            seg.hh.el = -54.3 * mV  # Reversal potential 
        self.dend.insert("pas")  # # Insert passive current in the dendrite  
        for seg in self.dend:   
            seg.pas.g = 0.001  # Passive conductance in S/cm2        
            seg.pas.e = -65 * mV  # Leak reversal potential             

    def __repr__(self):
        return "BallAndStick[{}]".format(self._gid)


my_cell = BallAndStick(0)


# Make sure soma is hh and dendtrite is passive membrane
for sec in h.allsec():
    print("%s: %s" % (sec, ", ".join(sec.psection()["density_mechs"].keys())))
    

# Stimulus    
stim = h.IClamp(my_cell.dend(1))  # at the origin of the dentrite
stim.delay = 5 #ms
stim.dur = 1 #ms
stim.amp = 0.1  # nA


soma_v = h.Vector().record(my_cell.soma(0.5)._ref_v)  # this can be plotted directly
dend_v=h.Vector().record(my_cell.dend(0.5)._ref_v)
t = h.Vector().record(h._ref_t)

h.finitialize(-65 * mV) # initialize membrane potential  
h.continuerun(25 * ms) # run until time 25 ms:
    
    
plt.figure()
plt.plot(t, soma_v)
plt.xlabel("t (ms)")
plt.ylabel("v (mV)")
plt.show()


## For differnt values of stimulus input current
  
amps = [0.075 * i for i in range(1, 5)]  # [0.075, 0.15, 0.225, 0.3]
colors = ["green", "blue", "red", "black"]
labels = [round(k,4) for k in amps]

# Create a figure and axis using plt.subplots
fig, ax = plt.subplots()

for amp, color, label in zip(amps, colors, labels):
    stim.amp = amp
    h.finitialize(-65 * mV)
    h.continuerun(25 * ms)
    ax.plot(t, list(soma_v), color=color, label=label)  # Use ax.plot instead of plt.plot 
 
ax.set_xlabel("Time (ms)",fontsize=20)
ax.set_ylabel("Voltage (mV)",fontsize=20)
ax.tick_params(axis='both', labelsize=16) 
ax.spines[['top','right']].set_visible(False) 
ax.legend(title='Stim. Amp (nA)', title_fontsize=16, frameon=False) 
plt.show()

  
# Tutorial example along with dendritic current   
amps = [0.075 * i for i in range(1, 5)]  # [0.075, 0.15, 0.225, 0.3]
colors = ["green", "blue", "red", "black"]
labels = [round(k, 4) for k in amps] 
fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axis using plt.subplots 
for amp, color, label in zip(amps, colors, labels):
    stim.amp = amp
    h.finitialize(-65 * mV)
    h.continuerun(25 * ms)
    ax.plot(t, list(soma_v), color=color, label= label )
    ax.plot(t, list(dend_v), color=color, linestyle="--")

# Create a separate legend for soma and dendritic currents
custom_lines = [
    Line2D([0], [0], color="black", linestyle="-", label="Soma Voltage"),
    Line2D([0], [0], color="black", linestyle="--", label="Dendritic Voltage")
]

# Add the amplitude legend
first_legend = ax.legend(title='Stim. Amp (nA)', title_fontsize=16, fontsize=16, loc='upper right',frameon=False,bbox_to_anchor=(0.8, 1.0)) 
# Add the custom legend for signal types
ax.add_artist(first_legend)
ax.legend(handles=custom_lines, title="Signal Type",fontsize=16,  title_fontsize=16, loc='upper right',frameon=False,bbox_to_anchor=(0.85, 0.5))

ax.set_xlabel("Time (ms)", fontsize=20)
ax.set_ylabel("Voltage (mV)", fontsize=20)
ax.tick_params(axis='both', labelsize=16)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.show()



# Why the below is differnt from above?  
amps = [0.02,0.05,0.075,0.1,0.15]
colors = ["cyan","green", "blue", "red", "black"]
labels=[str(round(k,4)) for k in amps]

fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axis using plt.subplots 
for amp, color, label in zip(amps, colors, labels):
    stim.amp = amp
    h.finitialize(-65 * mV)
    h.continuerun(25 * ms)
    ax.plot(t, list(soma_v), color=color, label= label )
    ax.plot(t, list(dend_v), color=color, linestyle="--")

# Create a separate legend for soma and dendritic currents
custom_lines = [
    Line2D([0], [0], color="black", linestyle="-", label="Soma Voltage"),
    Line2D([0], [0], color="black", linestyle="--", label="Dendritic Voltage")
]

# Add the amplitude legend
first_legend = ax.legend(title='Stim. Amp (nA)', title_fontsize=16, fontsize=16, loc='upper right',frameon=False,bbox_to_anchor=(0.8, 1.0)) 
# Add the custom legend for signal types
ax.add_artist(first_legend)
ax.legend(handles=custom_lines, title="Signal Type",fontsize=16,  title_fontsize=16, loc='upper right',frameon=False,bbox_to_anchor=(0.85, 0.5))

ax.set_xlabel("Time (ms)", fontsize=20)
ax.set_ylabel("Voltage (mV)", fontsize=20)
ax.tick_params(axis='both', labelsize=16)
ax.spines[['top', 'right']].set_visible(False)

plt.tight_layout()
plt.show()

  


## Role of number of segments (nseg)   
amps = [0.075 * i for i in range(1, 5)]
colors = ["green", "blue", "red", "black"]
labels=[str(round(k,4)) for k in amps]

fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axis using plt.subplots  
for amp, color,label in zip(amps, colors,labels):  # Like in previous simulation
    stim.amp = amp
    for my_cell.dend.nseg, width in [(1, 2), (101, 1)]:  # Segments and width
        h.finitialize(-65)
        h.continuerun(25)
        ax.plot(t, list(soma_v),   color=color,linewidth =width,label=label)
        ax.plot(t, list(dend_v),  linestyle="dashed", color=color,linewidth=width) 
# Create a separate legend for soma and dendritic currents
custom_lines = [
    Line2D([0], [0], color="black", linestyle="-", label="Soma Voltage"),
    Line2D([0], [0], color="black", linestyle="--", label="Dendritic Voltage")
]

# Add the amplitude legend
first_legend = ax.legend(title='Stim. Amp (nA)', title_fontsize=16, fontsize=16, loc='upper right',frameon=False,bbox_to_anchor=(0.8, 1.0)) 
# Add the custom legend for signal types
ax.add_artist(first_legend)
ax.legend(handles=custom_lines, title="Signal Type",fontsize=16,  title_fontsize=16, loc='upper right',frameon=False,bbox_to_anchor=(0.85, 0.5))  
        
ax.set_xlabel("Time (ms)", fontsize=20)
ax.set_ylabel("Voltage (mV)", fontsize=20)
ax.tick_params(axis='both', labelsize=16)
ax.spines[['top', 'right']].set_visible(False)  
 
plt.tight_layout()
plt.show() 