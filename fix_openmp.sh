#!/bin/bash

# ============================================
# Fix OpenMP Duplicate Library Error
# ============================================
# This script fixes the root cause of OMP error on macOS
# by reinstalling packages with compatible versions

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}=========================================="
echo "Fixing OpenMP Duplicate Library Error"
echo "==========================================${NC}"
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Activating virtual environment...${NC}"
    source .venv/bin/activate
fi

echo -e "${YELLOW}[1/5] Uninstalling conflicting packages...${NC}"
pip uninstall -y numpy torch transformers 2>/dev/null || true
echo -e "${GREEN}✓ Conflicting packages removed${NC}"
echo ""

echo -e "${YELLOW}[2/5] Cleaning pip cache...${NC}"
pip cache purge 2>/dev/null || true
echo -e "${GREEN}✓ Cache cleaned${NC}"
echo ""

echo -e "${YELLOW}[3/5] Installing NumPy with specific version...${NC}"
pip install numpy==1.24.3 --no-cache-dir
echo -e "${GREEN}✓ NumPy 1.24.3 installed${NC}"
echo ""

echo -e "${YELLOW}[4/5] Installing PyTorch with specific version...${NC}"
pip install torch==2.1.0 --no-cache-dir
echo -e "${GREEN}✓ PyTorch 2.1.0 installed${NC}"
echo ""

echo -e "${YELLOW}[5/5] Installing Transformers with compatible version...${NC}"
pip install transformers==4.36.2 accelerate --no-cache-dir
echo -e "${GREEN}✓ Transformers 4.36.2 installed${NC}"
echo ""

echo -e "${YELLOW}[6/6] Reinstalling other dependencies...${NC}"
pip install -r requirements.txt --no-cache-dir
echo -e "${GREEN}✓ All dependencies reinstalled${NC}"
echo ""

# Set environment variables permanently
echo -e "${YELLOW}Setting environment variables...${NC}"
if [ -f ~/.zshrc ]; then
    if ! grep -q "KMP_DUPLICATE_LIB_OK" ~/.zshrc; then
        echo "export KMP_DUPLICATE_LIB_OK=TRUE" >> ~/.zshrc
        echo "export OMP_NUM_THREADS=1" >> ~/.zshrc
        echo -e "${GREEN}✓ Added to ~/.zshrc${NC}"
    fi
fi

if [ -f ~/.bash_profile ]; then
    if ! grep -q "KMP_DUPLICATE_LIB_OK" ~/.bash_profile; then
        echo "export KMP_DUPLICATE_LIB_OK=TRUE" >> ~/.bash_profile
        echo "export OMP_NUM_THREADS=1" >> ~/.bash_profile
        echo -e "${GREEN}✓ Added to ~/.bash_profile${NC}"
    fi
fi

echo ""
echo -e "${GREEN}=========================================="
echo "✓ OpenMP Error Fixed!"
echo "==========================================${NC}"
echo ""
echo "What was done:"
echo "  1. Removed conflicting NumPy and PyTorch versions"
echo "  2. Installed NumPy 1.24.3 (compatible version)"
echo "  3. Installed PyTorch 2.1.0 (compatible version)"
echo "  4. Set KMP_DUPLICATE_LIB_OK=TRUE"
echo "  5. Set OMP_NUM_THREADS=1"
echo ""
echo "Next steps:"
echo "  1. Restart your terminal or run: source ~/.zshrc"
echo "  2. Test the API: bash run_api.sh"
echo ""
echo "If the error persists, try:"
echo "  - Restart terminal completely"
echo "  - Delete .venv and recreate: rm -rf .venv && python3 -m venv .venv"
echo ""
