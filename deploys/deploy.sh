#!/usr/bin/env bash

# main script for deploying app

set -euo pipefail

main() {
    local SCRIPT_DIR
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    local PROJECT_DIR
    PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

    cd "$PROJECT_DIR"

    bef_commit_hash="$(git rev-parse --short HEAD)"

    git pull --ff-only

    af_commit_hash="$(git rev-parse --short HEAD)"

    echo "Nasazuji: $bef_commit_hash -> $af_commit_hash"

    if [[ "$bef_commit_hash" == "$af_commit_hash" ]]; then
        echo "stejné"
    else
        echo "jiné"
    fi

    echo "Buildim a spoustim kontejnery"

    docker compose up -d --build

    docker compose restart nginx

    # Delete old docker images -f (means force)
    docker image prune -f


    # Loop for verification if site is working
    for i in {1..30}; do
        echo "Pokus $i"

        # fail: when HTTP error return non null exit code
        # s: silent, S: show error, o: web content into /dev/null
        if curl -fsS -o /dev/null https://taskhub.tomas-dev.cz/ && curl -fsS -o /dev/null https://taskhub.tomas-dev.cz/api/admin/login/; then
            echo "Webovka je funkční"

            return 0 # Stops whole function main
        else
            sleep 2
        fi
    done

    echo "CHYBA: web neodpovida ani po 30 pokusech" >&2

    # show docker error logs
    docker compose logs --tail=30 backend

    return 1
}

main "$@"; exit