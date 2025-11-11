#!/bin/bash

# Script de despliegue automático
echo "🚀 Iniciando despliegue del Sistema de Empleados..."

# Actualizar sistema
echo "📦 Actualizando sistema..."
sudo yum update -y  # Para Amazon Linux
# sudo apt-get update && sudo apt-get upgrade -y  # Para Ubuntu

# Instalar Docker
echo "🐳 Instalando Docker..."
sudo yum install -y docker  # Amazon Linux
# sudo apt-get install -y docker.io  # Ubuntu

# Iniciar y habilitar Docker
echo "🔧 Configurando Docker..."
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Instalar Docker Compose
echo "📋 Instalando Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Crear directorio de la aplicación
echo "📁 Configurando directorio de la aplicación..."
mkdir -p /home/ec2-user/empleados-crud
cd /home/ec2-user/empleados-crud

# Esperar a que el usuario esté en el grupo docker
echo "⏳ Esperando configuración de Docker..."
sleep 10

# Clonar o copiar archivos (aquí copiarás manualmente tus archivos)
echo "✅ Sistema listo para recibir archivos de la aplicación"
echo "📝 Copia tus archivos a: /home/ec2-user/empleados-crud/"