// Funções para o Sistema de Gestão de T.I. CCB

document.addEventListener('DOMContentLoaded', function() {
    // Toggle do Sidebar
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    const content = document.getElementById('content');
    
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            content.classList.toggle('with-sidebar');
        });
    }
    
    // Auto-fechamento dos alertas após 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });
    
    // Preview de imagens para uploads
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(function(input) {
        input.addEventListener('change', function(e) {
            const previewContainer = document.createElement('div');
            previewContainer.classList.add('file-preview', 'mt-2');
            
            // Limpa previews anteriores
            const existingPreview = input.parentElement.querySelector('.file-preview');
            if (existingPreview) {
                existingPreview.remove();
            }
            
            if (this.files.length > 0) {
                const fileList = document.createElement('ul');
                fileList.classList.add('list-group');
                
                for (let i = 0; i < this.files.length; i++) {
                    const file = this.files[i];
                    const listItem = document.createElement('li');
                    listItem.classList.add('list-group-item', 'd-flex', 'justify-content-between', 'align-items-center');
                    
                    // Ícone baseado no tipo de arquivo
                    let icon = 'fa-file';
                    if (file.type.startsWith('image/')) {
                        icon = 'fa-file-image';
                    } else if (file.type.includes('pdf')) {
                        icon = 'fa-file-pdf';
                    } else if (file.type.includes('word')) {
                        icon = 'fa-file-word';
                    } else if (file.type.includes('excel') || file.type.includes('sheet')) {
                        icon = 'fa-file-excel';
                    } else if (file.type.includes('text')) {
                        icon = 'fa-file-alt';
                    }
                    
                    // Tamanho do arquivo formatado
                    const fileSize = formatFileSize(file.size);
                    
                    listItem.innerHTML = `
                        <span><i class="fas ${icon}"></i> ${file.name}</span>
                        <span class="badge bg-primary">${fileSize}</span>
                    `;
                    
                    fileList.appendChild(listItem);
                }
                
                previewContainer.appendChild(fileList);
                input.parentElement.appendChild(previewContainer);
            }
        });
    });
    
    // Editor de texto para a base de conhecimento
    const contentTextarea = document.querySelector('textarea[name="content"]');
    if (contentTextarea) {
        // Adiciona botões de formatação avançada
        const editorToolbar = document.createElement('div');
        editorToolbar.classList.add('editor-toolbar', 'mb-2');
        editorToolbar.innerHTML = `
            <div class="btn-group mb-2 me-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="bold" title="Negrito"><i class="fas fa-bold"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="italic" title="Itálico"><i class="fas fa-italic"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="strikethrough" title="Tachado"><i class="fas fa-strikethrough"></i></button>
            </div>
            <div class="btn-group mb-2 me-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="heading1" title="Título Grande"><i class="fas fa-heading"></i>1</button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="heading2" title="Título Médio"><i class="fas fa-heading"></i>2</button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="heading3" title="Título Pequeno"><i class="fas fa-heading"></i>3</button>
            </div>
            <div class="btn-group mb-2 me-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="unorderedList" title="Lista com Marcadores"><i class="fas fa-list-ul"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="orderedList" title="Lista Numerada"><i class="fas fa-list-ol"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="indent" title="Aumentar Recuo"><i class="fas fa-indent"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="outdent" title="Diminuir Recuo"><i class="fas fa-outdent"></i></button>
            </div>
            <div class="btn-group mb-2 me-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="link" title="Link"><i class="fas fa-link"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="image" title="Imagem"><i class="fas fa-image"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="table" title="Tabela"><i class="fas fa-table"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="code" title="Código"><i class="fas fa-code"></i></button>
            </div>
            <div class="btn-group mb-2">
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="alignLeft" title="Alinhar à Esquerda"><i class="fas fa-align-left"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="alignCenter" title="Centralizar"><i class="fas fa-align-center"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="alignRight" title="Alinhar à Direita"><i class="fas fa-align-right"></i></button>
                <button type="button" class="btn btn-sm btn-outline-secondary" data-format="alignJustify" title="Justificar"><i class="fas fa-align-justify"></i></button>
            </div>
        `;
        
        contentTextarea.parentElement.insertBefore(editorToolbar, contentTextarea);
        
        // Adiciona uma prévia do conteúdo formatado
        const previewContainer = document.createElement('div');
        previewContainer.classList.add('content-preview', 'mt-3', 'p-3', 'border', 'rounded');
        previewContainer.style.display = 'none';
        
        const previewToggle = document.createElement('button');
        previewToggle.type = 'button';
        previewToggle.classList.add('btn', 'btn-sm', 'btn-outline-primary', 'mt-2');
        previewToggle.innerHTML = '<i class="fas fa-eye"></i> Mostrar Prévia';
        previewToggle.addEventListener('click', function() {
            if (previewContainer.style.display === 'none') {
                previewContainer.innerHTML = contentTextarea.value;
                previewContainer.style.display = 'block';
                this.innerHTML = '<i class="fas fa-eye-slash"></i> Ocultar Prévia';
            } else {
                previewContainer.style.display = 'none';
                this.innerHTML = '<i class="fas fa-eye"></i> Mostrar Prévia';
            }
        });
        
        contentTextarea.parentElement.appendChild(previewToggle);
        contentTextarea.parentElement.appendChild(previewContainer);
        
        // Adiciona eventos aos botões
        const formatButtons = editorToolbar.querySelectorAll('button');
        formatButtons.forEach(button => {
            button.addEventListener('click', function() {
                const format = this.getAttribute('data-format');
                const textarea = contentTextarea;
                const start = textarea.selectionStart;
                const end = textarea.selectionEnd;
                const selectedText = textarea.value.substring(start, end);
                let replacement = '';
                
                switch(format) {
                    case 'bold':
                        replacement = `<strong>${selectedText}</strong>`;
                        break;
                    case 'italic':
                        replacement = `<em>${selectedText}</em>`;
                        break;
                    case 'strikethrough':
                        replacement = `<s>${selectedText}</s>`;
                        break;
                    case 'heading1':
                        replacement = `<h1>${selectedText}</h1>`;
                        break;
                    case 'heading2':
                        replacement = `<h2>${selectedText}</h2>`;
                        break;
                    case 'heading3':
                        replacement = `<h3>${selectedText}</h3>`;
                        break;
                    case 'unorderedList':
                        const ulItems = selectedText.split('\n');
                        replacement = '<ul>\n';
                        ulItems.forEach(item => {
                            if (item.trim() !== '') {
                                replacement += `  <li>${item.trim()}</li>\n`;
                            }
                        });
                        replacement += '</ul>';
                        break;
                    case 'orderedList':
                        const olItems = selectedText.split('\n');
                        replacement = '<ol>\n';
                        olItems.forEach(item => {
                            if (item.trim() !== '') {
                                replacement += `  <li>${item.trim()}</li>\n`;
                            }
                        });
                        replacement += '</ol>';
                        break;
                    case 'link':
                        const url = prompt('Digite a URL:', 'https://');
                        if (url) {
                            replacement = `<a href="${url}" target="_blank">${selectedText || url}</a>`;
                        } else {
                            return;
                        }
                        break;
                    case 'image':
                        const imgUrl = prompt('Digite a URL da imagem:', 'https://');
                        const imgAlt = prompt('Digite a descrição da imagem:', '');
                        if (imgUrl) {
                            replacement = `<img src="${imgUrl}" alt="${imgAlt}" class="img-fluid">`;
                        } else {
                            return;
                        }
                        break;
                    case 'table':
                        const rows = prompt('Número de linhas:', '3');
                        const cols = prompt('Número de colunas:', '3');
                        if (rows && cols) {
                            replacement = '<table class="table table-bordered">\n';
                            replacement += '  <thead>\n    <tr>\n';
                            for (let i = 0; i < parseInt(cols); i++) {
                                replacement += `      <th>Cabeçalho ${i+1}</th>\n`;
                            }
                            replacement += '    </tr>\n  </thead>\n  <tbody>\n';
                            for (let i = 0; i < parseInt(rows); i++) {
                                replacement += '    <tr>\n';
                                for (let j = 0; j < parseInt(cols); j++) {
                                    replacement += `      <td>Célula ${i+1}-${j+1}</td>\n`;
                                }
                                replacement += '    </tr>\n';
                            }
                            replacement += '  </tbody>\n</table>';
                        } else {
                            return;
                        }
                        break;
                    case 'code':
                        replacement = `<pre><code>${selectedText}</code></pre>`;
                        break;
                    case 'alignLeft':
                        replacement = `<div style="text-align: left;">${selectedText}</div>`;
                        break;
                    case 'alignCenter':
                        replacement = `<div style="text-align: center;">${selectedText}</div>`;
                        break;
                    case 'alignRight':
                        replacement = `<div style="text-align: right;">${selectedText}</div>`;
                        break;
                    case 'alignJustify':
                        replacement = `<div style="text-align: justify;">${selectedText}</div>`;
                        break;
                    case 'indent':
                        replacement = `<blockquote>${selectedText}</blockquote>`;
                        break;
                    case 'outdent':
                        // Remove blockquote se existir
                        if (selectedText.startsWith('<blockquote>') && selectedText.endsWith('</blockquote>')) {
                            replacement = selectedText.substring(12, selectedText.length - 13);
                        } else {
                            replacement = selectedText;
                        }
                        break;
                }
                
                textarea.value = textarea.value.substring(0, start) + replacement + textarea.value.substring(end);
                textarea.focus();
                textarea.selectionStart = start + replacement.length;
                textarea.selectionEnd = start + replacement.length;
                
                // Atualiza a prévia se estiver visível
                if (previewContainer.style.display !== 'none') {
                    previewContainer.innerHTML = textarea.value;
                }
            });
        });
    }
    
    // Função para formatar o tamanho do arquivo
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
    
    // Confirmação para ações de exclusão
    const deleteButtons = document.querySelectorAll('[data-confirm]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const message = this.getAttribute('data-confirm') || 'Tem certeza que deseja realizar esta ação?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
    
    // Filtro para tabelas
    const tableFilter = document.getElementById('tableFilter');
    if (tableFilter) {
        tableFilter.addEventListener('keyup', function() {
            const filterValue = this.value.toLowerCase();
            const table = document.querySelector('.table');
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.indexOf(filterValue) > -1) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }
    
    // Rolagem automática para o chat de comentários
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});

// Adicionar após o DOMContentLoaded
document.querySelectorAll('.card, .alert').forEach(element => {
    element.classList.add('fade-in');
});
