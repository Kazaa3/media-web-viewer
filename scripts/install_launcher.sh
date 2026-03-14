#!/bin/bash
# =============================================================================
# Media Web Viewer - Installation Script
# =============================================================================
# Description: Installs the global launcher for Media Web Viewer
# Usage: ./install_launcher.sh
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Media Web Viewer - Global Launcher Installation${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if launcher exists
LAUNCHER_SOURCE="$HOME/.local/bin/media-viewer"
if [[ ! -f "${LAUNCHER_SOURCE}" ]]; then
    echo -e "${RED}✗ Error: Launcher script not found at ${LAUNCHER_SOURCE}${NC}"
    echo "  Please ensure the launcher was created correctly."
    exit 1
fi

echo -e "${GREEN}✓${NC} Launcher script found: ${LAUNCHER_SOURCE}"

# Make executable
chmod +x "${LAUNCHER_SOURCE}"
echo -e "${GREEN}✓${NC} Launcher made executable"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo -e "${YELLOW}⚠${NC}  ~/.local/bin is not in your PATH"
    echo ""
    echo "To add it permanently, add this line to your shell configuration:"
    echo ""
    
    # Detect shell
    SHELL_NAME=$(basename "$SHELL")
    case "$SHELL_NAME" in
        bash)
            SHELL_RC="$HOME/.bashrc"
            ;;
        zsh)
            SHELL_RC="$HOME/.zshrc"
            ;;
        *)
            SHELL_RC="$HOME/.profile"
            ;;
    esac
    
    echo -e "${BLUE}  export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
    echo ""
    echo "File to edit: ${SHELL_RC}"
    echo ""
    
    # Ask if user wants to add it automatically
    read -p "Add to ${SHELL_RC} automatically? (y/n) " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        # Check if line already exists
        if grep -q 'PATH.*\.local/bin' "${SHELL_RC}" 2>/dev/null; then
            echo -e "${YELLOW}⚠${NC}  PATH entry already exists in ${SHELL_RC}"
        else
            echo "" >> "${SHELL_RC}"
            echo "# Added by Media Web Viewer installer" >> "${SHELL_RC}"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "${SHELL_RC}"
            echo -e "${GREEN}✓${NC} Added PATH configuration to ${SHELL_RC}"
            echo ""
            echo -e "${YELLOW}Note:${NC} Restart your terminal or run:"
            echo -e "  ${BLUE}source ${SHELL_RC}${NC}"
        fi
    else
        echo -e "${YELLOW}→${NC} Manual configuration needed"
    fi
else
    echo -e "${GREEN}✓${NC} ~/.local/bin is already in PATH"
fi

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Installation completed successfully!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo "Usage:"
echo "  media-viewer          - Start the application"
echo "  media-viewer --test   - Run validation tests"
echo "  media-viewer --help   - Show help message"
echo ""
echo "Or use the full path:"
echo "  ~/.local/bin/media-viewer"
echo ""

# Run test if PATH is available
if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
    echo "Running quick validation test..."
    echo ""
    media-viewer --test
fi
