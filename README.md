
<p align="left">
  <img src="https://img.shields.io/badge/status-active-brightgreen.svg" alt="status">
  <img src="https://img.shields.io/badge/contributions-welcome-blueviolet.svg" alt="contributions welcome">
  <img src="https://img.shields.io/badge/license-BSD-lightgrey.svg" alt="license">
</p>

# 🧠 NeuroSource  
### *A living, open catalogue of neural foundation models.*

> **NeuroSource** is a community-curated repository of **baseline and foundation models for neural data** — EEG, fMRI, ECoG, spikes, and beyond.  
> The goal: to build an evolving, transparent, and machine-readable map of how brain-AI models are built, shared, and reused.

---

## 🧩 Why this exists

Neural data research is exploding — but tracking *which models exist*, *what data they use*, and *how they connect* is hard.  
**NeuroSource** makes that knowledge structured, searchable, and open.

Think of it as:

> 🗺️ *“Papers with Code” for neural foundation models.*

Each model is described by a lightweight YAML file with consistent metadata (architecture, modality, dataset, year, links, etc.).  
Anyone can contribute — labs, students, or readers of new papers.

---

## 📁 Repository Structure

<pre>
neurosource/
├─ schema/        # JSON schema defining model fields
├─ models/        # Model entries organized by modality
│  ├─ eeg/
│  ├─ fmri/
│  ├─ ecog/
│  └─ other/
└─ papers/        # Optional paper summaries or notes
</pre>

---

## 🧠 Example Entry

`models/eeg/eegnet_2018.yaml`

```yaml
model_name: EEGNet
modality: EEG
architecture: CNN
task: classification
year: 2018
paper_url: https://arxiv.org/abs/1611.08024
code_url: https://github.com/vlawhern/arl-eegmodels
dataset_tags: [BNCI2014-001]
open_weights: false
notes: "Lightweight CNN baseline widely used for EEG decoding."
```

---

## 💡 How to Contribute

1. **Fork** this repo  
2. **Add your model**
   - Create a new file under `models/<modality>/<model_name>_<year>.yaml`
   - Follow the schema in `/schema/model.schema.json`
3. **Open a Pull Request**

Each PR is automatically checked for:
- ✅ Correct field names / formatting  
- ✅ Valid URLs  
- ✅ Consistency with schema  

Once approved, it appears in the public index.

🧩 Want to add a paper instead?  
Add a short note in `/papers/<year>/yourpaper.md`.

---

## 🔍 Schema Overview

| Field | Type | Description |
|-------|------|--------------|
| model_name | string | Full name of the model |
| modality | string | EEG, fMRI, ECoG, spikes, etc. |
| architecture | string | CNN, Transformer, GraphNet... |
| task | string | classification, decoding, etc. |
| year | int | Year of publication |
| paper_url | string | Link to paper |
| code_url | string | Link to repo (if available) |
| dataset_tags | list | Datasets used |
| open_weights | bool | True if pretrained weights are public |
| notes | string | Freeform notes or context |

---

## 🌱 Roadmap


✅ MVP -------------  Launch repo + schema + seed models

🚧 Next ------------- Auto-generate Markdown index of models 

🧭 Later ------------- Integrate into NeuroSource meta-research dashboard

🌐 Future ------------- Interactive web explorer (GitHub Pages + JSON index)

---

## 🧩 Example Query Ideas (Future)

Once the data grows, we’ll be able to ask questions like…

> “Show all EEG foundation models released after 2023.”  
> “Which fMRI architectures reuse EEG pretraining?”  
> “How many open-weights models exist per modality?”

---

## 🤝 Contributing Labs & Individuals

We credit all contributors in **CONTRIBUTORS.md**.  
Your name is added automatically when your PR is merged!

---

## 🪶 Citation

If you use or reference **NeuroSource** in your work:

```bibtex
@misc{neurosource2025,
  title        = {NeuroSource: An Open Catalogue of Neural Foundation Models},
  author       = {Contributors to the NeuroSource Project},
  year         = {2025},
  howpublished = {\url{https://github.com/IVADO-NeuroAI/neurosource}}
}
```





