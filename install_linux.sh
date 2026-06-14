#!/bin/bash
# Linux Installation Script - AI Model Firewall as systemd service
# For corporate / server deployments

echo "🛡️ AI Model Firewall - Linux Servis Kurulumu"
echo "============================================"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Lütfen sudo ile çalıştırın: sudo bash install_linux.sh"
    exit 1
fi

USER_HOME=$(eval echo ~$SUDO_USER)
INSTALL_DIR="/opt/ai-model-firewall"

echo "[1/5] Gerekli paketler yükleniyor..."
apt-get update -qq
apt-get install -y -qq python3-pip python3-venv libnotify-bin

echo "[2/5] Kurulum dizini oluşturuluyor..."
mkdir -p "$INSTALL_DIR"
cp -r . "$INSTALL_DIR"
chown -R $SUDO_USER:$SUDO_USER "$INSTALL_DIR"

echo "[3/5] Python ortamı hazırlanıyor..."
cd "$INSTALL_DIR"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt --quiet

echo "[4/5] systemd servisi oluşturuluyor..."
cat > /etc/systemd/system/aimodelfirewall.service << EOF
[Unit]
Description=AI Model Firewall - Model Security Scanner
After=network.target

[Service]
Type=simple
User=$SUDO_USER
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/main.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

echo "[5/5] Servis aktifleştiriliyor..."
systemctl daemon-reload
systemctl enable aimodelfirewall.service
systemctl start aimodelfirewall.service

echo ""
echo "✅ Kurulum tamamlandı!"
echo ""
echo "Servis durumu kontrol etmek için:"
echo "  sudo systemctl status aimodelfirewall.service"
echo ""
echo "Logları görmek için:"
echo "  journalctl -u aimodelfirewall.service -f"
echo ""
echo "Durdurmak için:"
echo "  sudo systemctl stop aimodelfirewall.service"