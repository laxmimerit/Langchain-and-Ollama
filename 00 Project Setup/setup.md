# ML Environment Setup Guide
Setup for LangChain, LangGraph & Ollama with GPU support (Windows/Linux/Mac)

**Prerequisites:** Install Anaconda/Miniconda from https://www.anaconda.com/docs/getting-started/anaconda/install#basic-install-instructions

---

## 1. Check Conda
```bash
conda --version
conda env list
```

## 2. Create ML Environment
```bash
conda create -n ml python=3.12 -y
```

## 3. Disable Base Auto-Activation
```bash
conda config --set auto_activate_base false
```

## 4. Setup ML Auto-Activation

### Windows PowerShell
```powershell
# Create/edit profile
notepad $PROFILE
# If error: New-Item -Path $PROFILE -Type File -Force

# Add this line:
conda activate ml

# Save, then reload
. $PROFILE
```

### Linux/Mac
```bash
# For Bash - edit ~/.bashrc
# For Zsh - edit ~/.zshrc
nano ~/.bashrc  # or ~/.zshrc

# Add this line:
conda activate ml

# Save and reload
source ~/.bashrc  # or ~/.zshrc
```

## 5. Activate Environment
```bash
conda activate ml
```

## 6. Navigate to Project
```bash
cd path/to/your/project
```

## 7. Install Requirements
```bash
pip install -r requirements.txt
```

## 8. Install PyTorch
Visit https://pytorch.org/get-started/locally/

Select the latest PyTorch and Install.

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu128
```

## 9. Verify GPU
```python
import torch
torch.cuda.is_available()  # Should return True
torch.cuda.get_device_name(0)  # Shows GPU name
exit()
```

## 10. Setup Jupyter Kernel
1. Open notebook in VS Code
2. Install ipykernel if prompted
3. Select kernel: `ml (Python 3.12.4)`
4. Test: `import torch; torch.cuda.is_available()`

---

## Troubleshooting

**Conda not recognized:**
- **Windows:** Add Conda to PATH
  1. Find Anaconda/Miniconda installation path (usually `C:\Users\YourName\anaconda3` or `C:\ProgramData\anaconda3`)
  2. Add these paths to System Environment Variables:
     - `C:\Users\YourName\anaconda3`
     - `C:\Users\YourName\anaconda3\Scripts`
     - `C:\Users\YourName\anaconda3\Library\bin`
  3. Restart terminal/PowerShell
  4. Or use Anaconda Prompt instead
- **Linux/Mac:** Initialize conda
  ```bash
  source ~/anaconda3/bin/activate  # or ~/miniconda3/bin/activate
  conda init bash  # or conda init zsh
  ```
  Then restart terminal

**GPU not detected:**
- Check drivers: `nvidia-smi`
- Reinstall PyTorch with correct CUDA version

**PowerShell execution error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Kernel not showing:**
```bash
pip install ipykernel
python -m ipykernel install --user --name ml
```

---

## Quick Commands
```bash
conda env list              # List environments
conda activate ml           # Activate
conda deactivate           # Deactivate
pip list                   # List packages
```
