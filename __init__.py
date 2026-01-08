import localPing
import query

query.inicializar_banco()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        print("=" * 60)
        print("DEVICE FINDER - Coleta de Dados")
        print("=" * 60)
        
        if localPing.verificar_internet() == 0:
            print("\n⚠ Aviso: Sem conexão com a internet. Alguns dados podem estar ausentes.")
        else:
            print("\n✅ Conexão com a internet estabelecida.\n")
        
        dados_pings = localPing.montar_json_completo()
        
        import json
        print(json.dumps(dados_pings, indent=4, ensure_ascii=False))
        
        sucesso, mensagem = query.inserir_ping(dados_pings)
        print(f"\n{mensagem}")
    else:
        from app_gui import main
        main()