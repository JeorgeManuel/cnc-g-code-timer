# **CNC Machining Time Calculator**

A Python-based tool for estimating machining time directly from G-code.
The program parses linear moves, arcs (G2/G3), and helical toolpaths to calculate the actual 3D distance traveled by the cutter, and converts this into total machining time based on feed rates.

---

## **📌 Features**

### **✔ G-code Parser**

* Supports `G0`, `G1`, `G2`, `G3` toolpath commands
* Extracts X, Y, Z coordinates
* Extracts feed rate `F`
* Reads arc centers `I`, `J` and calculates radius

### **✔ Linear Interpolation**

Computes movement distance using Euclidean distance between discrete points.

### **✔ Circular Interpolation**

Accurate arc length calculation using cosine rule:

* Handles CW (`G2`) and CCW (`G3`)
* Includes floating-point compensation (clamping) to avoid acos domain errors
* Supports multi-quadrant arcs

### **✔ Helical Moves**

Generalized arc calculation for spiral paths:

* Detects Z changes during G2/G3
* Computes true 3D helical segment length
* Uses formula:

  ```
  L = sqrt(L_xy² + Δz²)
  ```

### **✔ Total Machine Time**

For each G-code motion:

* Compute distance
* Divide by feed rate
* Accumulate total machining time
* Converts to human-readable format (HH:MM:SS)

---

## **🖥 GUI Interface**

Includes a simple Tkinter/CustomTkinter-based interface:

* Upload `.nc` / G-code files
* Displays machining time result
* Embeds project logo
* Future expansion planned for:

  * File drag-and-drop
  * Visual path preview
  * Multi-axis support

---

## **📂 Repository Structure**

Example structure (your repo may differ):

```
├── main.py                # GUI + logic entry point
├── timerlogic.py          # Modular time calculations
├── assets/
│   └── logo.png
├── gcode_samples/
│   └── example.nc
└── README.md
```

---

## **🧮 Mathematical Details**

### **Linear Moves (G0/G1)**

```
L = sqrt(Δx² + Δy² + Δz²)
```

### **Circular/Arc Moves (G2/G3)**

Using chord length and arc radius:

```
AB = sqrt(Δx² + Δy²)
r = sqrt(I² + J²)
cos(θ) = (2r² − AB²) / (2r²)
θ = acos(clamped_value)
L = r * θ
```

### **Helical Moves**

When Z changes during G2/G3:

```
L_xy = r * θ
L_helix = sqrt( L_xy² + Δz² )
```

---

## **🐞 Known Issues**

* Arc direction (CW vs CCW) currently assumes shortest path
* No R-value arc support yet (only I/J)
* No G-code modal state handling for omitted coordinates
* Limited error messaging in GUI

---

## **🚀 Future Enhancements**

* Better G-code state machine (modal groups)
* Visualization of toolpath in matplotlib or a 3D viewer
* Support for:

  * G41/G42 cutter compensation
  * G43 tool length offsets
  * R-based arc definitions


---

## **📄 License**

MIT License (or your preferred license)

---

## **🤝 Contributing**

Pull requests are welcome.
For major changes, please open an issue to discuss your idea first.

---

## **📬 Contact**

Created by **Jeorge Manuel**
SARAO Electronics Intern
Email: `jmanuel@sarao.ac.za` or `jeorgemanuel04@gmail.com`
